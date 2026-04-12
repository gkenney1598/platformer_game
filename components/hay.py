from pyray import *
from settings import *

class Hay:
    def __init__(self, x, y):
        # Position (top-left for collision)
        self.rect = Rectangle(x, y, TILE_SIZE * 0.7, TILE_SIZE * 0.7)

    def startup(self):
        pass

    def update(self):
        pass

    def draw(self):
        draw_rectangle_rec(self.rect, YELLOW)

    def shutdown(self):
        pass