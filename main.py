import random

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel

Window.size = (1280, 720)
tile_size = Window.width/16

class SortWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reset()
        Clock.schedule_interval(self.every_frame, 0)

    def reset(self):
        self.canvas.clear()
        self.canvas.add(Color(1,1,1))
        self.data = RandomData()
        for i in self.data.rectangles:
            self.canvas.add(i)
        self.j = 0
        self.i = 0
        self.key = self.data.rectangles[self.i].size[1]
        self.bubble_sorting = False
        self.insertion_sorting = False
        self.reset_text = self.add_text("Reset", tile_size / 2, Window.width / 2 - tile_size,
                                         tile_size, (2 * tile_size, tile_size))
        self.canvas.add(self.reset_text)
        self.bubble_text = self.add_text("Bubble", tile_size/2, Window.width/2 - 2*tile_size, Window.height - tile_size, (2*tile_size, tile_size))
        self.canvas.add(self.bubble_text)
        self.insertion_text = self.add_text("Insertion", tile_size / 2, Window.width / 2 - 6 * tile_size,
                                         Window.height - tile_size, (2 * tile_size, tile_size))
        self.canvas.add(self.insertion_text)


    def every_frame(self,dt):
        if self.bubble_sorting == True:
            self.bubble()
        if self.insertion_sorting == True:
            self.insertion()

    def on_touch_down(self, touch):
        if self.bubble_text.pos[0] < touch.x < self.bubble_text.pos[0] + self.bubble_text.size[0] and self.bubble_text.pos[1] < touch.y < self.bubble_text.pos[1] + self.bubble_text.size[1] :
            self.j = 0
            self.i = 0
            self.bubble_sorting = True
        if self.insertion_text.pos[0] < touch.x < self.insertion_text.pos[0] + self.insertion_text.size[0] and self.insertion_text.pos[1] < touch.y < self.insertion_text.pos[1] + self.insertion_text.size[1] :
            self.j = 0
            self.i = 1
            self.key = self.data.rectangles[self.i].size[1]
            self.insertion_sorting = True
        if self.reset_text.pos[0] < touch.x < self.reset_text.pos[0] + self.reset_text.size[0] and self.reset_text.pos[1] < touch.y < self.reset_text.pos[1] + self.reset_text.size[1] :
            self.reset()

    def bubble(self):
        if self.i < len(self.data.rectangles) - 1 - self.j:
            if self.data.rectangles[self.i].size[1] > self.data.rectangles[self.i + 1].size[1]:
                self.data.rectangles[self.i].size, self.data.rectangles[self.i+1].size = self.data.rectangles[self.i+1].size, self.data.rectangles[self.i].size
            self.i += 1
        if self.i == len(self.data.rectangles) - 1 - self.j:
            self.i = 0
            self.j += 1

    def insertion(self):
        if self.j >= 0 and self.key < self.data.rectangles[self.j].size[1]:
            self.data.rectangles[self.j+1].size = self.data.rectangles[self.j].size
            self.j -= 1
        elif self.i < len(self.data.rectangles)-1:
            self.data.rectangles[self.j + 1].size = (self.data.rectangles[self.j + 1].size[0], self.key)
            self.i += 1
            self.key = self.data.rectangles[self.i].size[1]
            self.j = self.i - 1


    def add_text(self, text, size, x, y, recsize):
        self.rect = Rectangle(pos=(x, y), size=recsize)
        label = CoreLabel(text=text, font_size=size)
        label.refresh()
        text = label.texture
        pos = (x, y)
        return Rectangle(size=text.size, pos=pos, texture=text)


class RandomData():
    def __init__(self):
        self.data = []
        for i in range(100): self.data.append(random.randrange(1000))
        self.rectangles = []
        for i in range(len(self.data)):
            self.rectangles.append(Rectangle(color=(0, 1, 0) ,pos=(tile_size + tile_size*0.14*i, tile_size*2),size=(0.13*tile_size, 0.005 * tile_size *self.data[i])))



sorting = SortWidget()

class SortingApp(App):

    def build(self):
        return sorting


if __name__ == "__main__":
    app = SortingApp()
    app.run()
