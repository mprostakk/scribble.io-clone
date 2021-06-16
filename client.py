import json
import socket
from queue import Queue
from json import dumps
from datetime import datetime
from threading import Thread


from kivy.clock import Clock
from kivy.app import App
from kivy.uix.stencilview import StencilView
from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line


from custom_request import Request
from utils import receive_request

q = Queue()
q_sender = Queue()


class PaintWidget(StencilView):
    def __init__(self, **kwargs):
        self.lines = list()
        self.k = 0
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        line = Line(points=(touch.x, touch.y))
        self.lines.append(line)
        touch.ud['line'] = line
        touch.ud['line_id'] = self.k
        self.k += 1

    def on_touch_move(self, touch):
        line = touch.ud.get('line')
        line_id = touch.ud.get('line_id')

        request = Request()
        request.headers['Action'] = 'DRAW'

        data = {
            'id': line_id,
            'x': int(touch.x),
            'y': int(touch.y)
        }

        request.headers['Data'] = json.dumps(data)
        q_sender.put(request)


class Screen(Widget):
    def __init__(self, **kwargs):
        event = Clock.schedule_interval(self.queue_callback, 1 / 300.)
        self.lines = dict()
        super().__init__(**kwargs)
        self.current_color = [1, 0, 0, 1]

    def set_color(self, color):
        r, g, b = color.split(',')
        self.current_color.clear()
        self.current_color.extend([int(r), int(g), int(b), 1])

    def send_message(self):
        text_input = self.ids.text_input
        text = text_input.text.strip()
        if text == '':
            return

        data_object = {'message': text}
        json_data = dumps(data_object)

        request = Request()
        request.headers['Action'] = 'SEND_MESSAGE'
        request.headers['Data'] = json_data
        q_sender.put(request)

        text_input.text = ''

    def queue_callback(self, dt):
        if q.empty() is False:
            request = q.get()
            q.task_done()
            self.custom_dispatch(request)

    def custom_dispatch(self, request):
        if request.action == 'UPDATE_CHAT':
            self.update_chat(request)
        elif request.action == 'UPDATE_POINTS':
            self.update_points(request)
        elif request.action == 'DRAW':
            self.update_drawing(request)
        elif request.action == 'CURRENT_WORD':
            self.update_current_word(request)
        elif request.action == 'NEW_ROUND':
            self.update_new_round(request)
        # elif request.action == 'CLEAR_CANVAS':
        #     self.clear_canvas()

    def update_chat(self, request):
        chat_grid = self.ids.chat_grid
        chat_grid.add_widget(
            Label(
                text=request.data['message']
            )
        )

    def update_new_round(self, request):
        # clear drawing
        self.update_current_word(request)
        self.clear_canvas()

    def update_points(self, request):
        point_layout = self.ids.point_layout

        while len(point_layout.children):
            point_layout.remove_widget(point_layout.children[0])

        for player in request.data['message']:
            username = player.get('username')
            points = player.get('points')

            point_layout.add_widget(
                Factory.UserLabel(
                    text=f'{username}: {points}'
                )
            )

    def update_drawing(self, request):
        paint_widget = self.ids.paint_widget

        line_id = request.data['id']
        x = request.data['x']
        y = request.data['y']

        line = self.lines.get(line_id)
        if line is None:
            with paint_widget.canvas:
                Color(*self.current_color)
                new_line = Line()
                new_line.points = [x, y]
                self.lines[line_id] = new_line
        else:
            line.points += [x, y]
        
    def clear_canvas(self):
        paint_widget = self.ids.paint_widget
        paint_widget.canvas.clear()
        self.lines = dict()

    def update_current_word(self, request):
        word = request.data['message']
        word_id = self.ids.word
        word_id.text = word


class TestApp(App):
    def build(self):
        return Screen()


def worker(s):
    while True:
        request = receive_request(s)
        q.put(request)


def worker_send(s):
    while True:
        request = q_sender.get()
        s.sendall(request.parse_headers().encode('utf-8'))
        q_sender.task_done()


if __name__ == '__main__':
    Window.size = (800, 600)
    Window.minimum_width, Window.minimum_height = Window.size

    host = 'localhost'
    port = 1782

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    worker_thread = Thread(target=worker, args=(s,))
    worker_thread.daemon = True
    worker_thread.start()

    sender_thread = Thread(target=worker_send, args=(s,))
    sender_thread.daemon = True
    sender_thread.start()

    TestApp().run()
