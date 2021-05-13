from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.stencilview import StencilView


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
        super().__init__(**kwargs)

    def send_message(self):
        text_input = self.ids.text_input
        text = text_input.text.strip()
        if text == '':
            return

        chat_grid = self.ids.chat_grid
        chat_grid.add_widget(
            Label(
                text=text
            )
        )
        text_input.text = ''

        paint = self.ids.paint_widget
        img = paint.export_as_image()
        print(img)

        paint.export_to_png('test.png')


class TestApp(App):
    def build(self):
        return Screen()


if __name__ == '__main__':
    Window.size = (800, 600)
    Window.minimum_width, Window.minimum_height = Window.size

    TestApp().run()
