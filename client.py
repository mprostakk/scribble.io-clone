import socket
from queue import Queue


from threading import Thread
from kivy.clock import Clock

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.stencilview import StencilView


q = Queue()
q_sender = Queue()


class PaintWidget(StencilView):
    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 0, 0)
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        line = touch.ud.get('line')
        if line:
            line.points += [touch.x, touch.y]


class Screen(Widget):
    def __init__(self, **kwargs):
        event = Clock.schedule_interval(self.test_callback, 1 / 30.)    
        super().__init__(**kwargs)

    def send_message(self):
        text_input = self.ids.text_input
        text = text_input.text.strip()
        if text == '':
            return

        q_sender.put(text)
        text_input.text = ''

        # paint = self.ids.paint_widget
        # img = paint.export_as_image()
        # print(img)
        # paint.export_to_png('test.png')
    
    def test_callback(self, dt):
        if q.empty() is False:
            data = q.get()
            q.task_done()

            chat_grid = self.ids.chat_grid
            chat_grid.add_widget(
                Label(
                    text=data
                )
            )

class TestApp(App):
    def build(self):
        return Screen()


def worker(s):
    while True:
        buffer = s.recv(100)
        print('Worker:')
        print(buffer.decode('utf-8'))
        q.put(buffer.decode('utf-8'))


def worker_send(s):
    while True:
        item = q_sender.get()
        print(item)
        message = f'Action: Test\r\nData: {item}\r\n\r\n'
        q_sender.task_done()
        s.sendall(message.encode('utf-8'))


def my_callback(dt):
        print('My callback is called', dt)


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

    # event = Clock.schedule_interval(my_callback, 1 / 30.)    

    TestApp().run()
