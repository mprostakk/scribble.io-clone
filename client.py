import socket
from queue import Queue
from json import dumps
from datetime import datetime

from threading import Thread
from kivy.clock import Clock

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.stencilview import StencilView

from custom_request import Request
from utils import receive_request

q = Queue()
q_sender = Queue()


class PaintWidget(StencilView):
    def __init__(self, **kwargs):
        self.lines = list()
        super().__init__(**kwargs)

    def on_touch_down(self, touch):
        line = Line(points=(touch.x, touch.y))
        self.lines.append(line)
        touch.ud['line'] = line

    def on_touch_move(self, touch):
        line = touch.ud.get('line')
        if line:
            line.points += [touch.x, touch.y]

        request = Request()
        request.headers['Action'] = 'DRAW'
        request.headers['Data'] = str([touch.x, touch.y])
        request.headers['Data'] = self.parse_lines()
        q_sender.put(request)

    def parse_lines(self):
        s = []
        for line in self.lines:
            s.append(line.points)

        return str(s)

class Screen(Widget):
    def __init__(self, **kwargs):
        event = Clock.schedule_interval(self.queue_callback, 1 / 300.)
        self.lines = []
        super().__init__(**kwargs)

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

    def update_chat(self, request):
        chat_grid = self.ids.chat_grid
        chat_grid.add_widget(
            Label(
                text=request.data['message']
            )
        )

    def update_points(self, request):
        point_layout = self.ids.point_layout

        while len(point_layout.children):
            point_layout.remove_widget(point_layout.children[0])

        for player in request.data['message']:
            username = player.get('username')
            points = player.get('points')

            point_layout.add_widget(
                Label(
                    text=f'{username}: {points}'
                )
            )

    def update_drawing(self, request):
        lines = request.data

        for pos in range(0, len(lines)):
            try:
                line_points = self.lines[pos]
                line_points.points = lines[pos]
            except IndexError:
                with self.canvas:
                    Color(1, 0, 0, 1)
                    new_line = Line()
                    new_line.points = lines[pos]
                    self.lines.append(new_line)


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
    port = 1781

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    worker_thread = Thread(target=worker, args=(s,))
    worker_thread.daemon = True
    worker_thread.start()

    sender_thread = Thread(target=worker_send, args=(s,))
    sender_thread.daemon = True
    sender_thread.start()

    TestApp().run()
