from pyray import *
from settings import *


class Vase:
    def __init__(self, x, y, full):
        self.rect = Rectangle(x, y, TILE_SIZE * 0.7, TILE_SIZE * 0.7)
        self.full = full


    def startup(self):
        pass
    def update(self):
        pass
    def draw(self):
        draw_rectangle_rec(self.rect, BROWN)
    def shutdown(self):
        pass