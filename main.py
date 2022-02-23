import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel

Window.size = (1280, 720)
tile_size = Window.width / 16


# klasa główna aplikacji
class SortWindow(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.sorting_widget = SortWidget()
        self.add_widget(self.sorting_widget)

        self.n_input = TextInput(text="N",multiline=False, font_size=30, size_hint=(0.1, 0.1), pos_hint={"x":0.2})
        self.add_widget(self.n_input)

        self.reset_btn = Button(text="Reset", font_size=30, size_hint=(0.1, 0.1), pos_hint={"x":0})
        self.reset_btn.bind(on_press=lambda x:self.sorting_widget.reset(int(self.n_input.text)))
        self.add_widget(self.reset_btn)

        self.start_btn = Button(text="Start", font_size=30, size_hint=(0.1, 0.1), pos_hint={"x":0.1})
        self.start_btn.bind(on_press=lambda x: self.sorting_widget.start_sorting())
        self.add_widget(self.start_btn)

class SortWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.merge_arr = []
        self.bubble_text = self.add_text("Bubble", tile_size / 2, Window.width / 2 - 2 * tile_size,
                                         Window.height - tile_size, (2 * tile_size, tile_size))
        self.insertion_text = self.add_text("Insertion", tile_size / 2, Window.width / 2 - 6 * tile_size,
                                            Window.height - tile_size, (2 * tile_size, tile_size))
        self.merge_text = self.add_text("Merge", tile_size / 2, Window.width / 2 + 2 * tile_size,
                                        Window.height - tile_size, (2 * tile_size, tile_size))
        self.reset(100)
        Clock.schedule_interval(self.every_frame, 0)

    # funkcja resetująca zbiory

    def reset(self, n):
        self.data = []
        self.merge_i = 0
        for i in range(n): self.data.append(random.randrange(1000))
        self.merge_arr = [self.data]
        self.reset_screen(self.data)
        self.j = 0
        self.i = 0
        self.key = self.data[1]
        self.bubble_sorting = False
        self.insertion_sorting = False
        self.merge_sorting = False

    # reset okna

    def reset_screen(self, data):
        self.canvas.clear()
        self.canvas.add(Color(1, 1, 1))
        j = 0
        for i in data:
            self.canvas.add(Rectangle(color=(0, 1, 0), pos=(tile_size + (Window.width-2*tile_size)/len(data) * j, tile_size * 2),
                                      size=((Window.width-2*tile_size)/len(data) - tile_size * 0.01, 0.005 * tile_size * i)))
            j += 1
        self.canvas.add(self.bubble_text)
        self.canvas.add(self.merge_text)
        self.canvas.add(self.insertion_text)

    # funkcja wyłowywana on every frame

    def every_frame(self, dt):
        if self.bubble_sorting:
            self.bubble()
            self.reset_screen(self.data)
        if self.insertion_sorting:
            self.insertion()
            self.reset_screen(self.data)

    def on_touch_down(self, touch):
        if self.bubble_text.pos[0] < touch.x < self.bubble_text.pos[0] + self.bubble_text.size[0] and \
                self.bubble_text.pos[1] < touch.y < self.bubble_text.pos[1] + self.bubble_text.size[1]:
            self.j = 0
            self.i = 0
            self.bubble_sorting = True
        if self.insertion_text.pos[0] < touch.x < self.insertion_text.pos[0] + self.insertion_text.size[0] and \
                self.insertion_text.pos[1] < touch.y < self.insertion_text.pos[1] + self.insertion_text.size[1]:
            self.j = 0
            self.i = 1
            self.key = self.data[self.i]
            self.insertion_sorting = True
        if self.merge_text.pos[0] < touch.x < self.merge_text.pos[0] + self.merge_text.size[0] and self.merge_text.pos[
            1] < touch.y < self.merge_text.pos[1] + self.merge_text.size[1]:
            pass

    def start_sorting(self):
        pass

    # sortowanie bąbelkowe

    def bubble(self):
        if self.i < len(self.data) - 1 - self.j:
            if self.data[self.i] > self.data[self.i + 1]:
                self.data[self.i], self.data[self.i + 1] = self.data[self.i + 1], self.data[self.i]
            self.i += 1
        if self.i == len(self.data) - 1 - self.j:
            self.i = 0
            self.j += 1

    # sortowanie przez wstawianie

    def insertion(self):
        if self.j >= 0 and self.key < self.data[self.j]:
            self.data[self.j + 1] = self.data[self.j]
            self.j -= 1
        elif self.i < len(self.data) - 1:
            self.data[self.j + 1] = self.key
            self.i += 1
            self.key = self.data[self.i]
            self.j = self.i - 1

    # dodawanie tekstu

    def add_text(self, text, size, x, y, recsize):
        self.rect = Rectangle(pos=(x, y), size=recsize)
        label = CoreLabel(text=text, font_size=size)
        label.refresh()
        text = label.texture
        pos = (x, y)
        return Rectangle(size=text.size, pos=pos, texture=text)

# deklaracja głównej klasy
sorting = SortWindow()


class SortingApp(App):

    def build(self):
        return sorting


if __name__ == "__main__":
    app = SortingApp()
    app.run()
