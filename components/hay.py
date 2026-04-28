from pyray import *
from settings import *

class Hay:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y + TILE_SIZE * 0.3, TILE_SIZE, TILE_SIZE * 0.7)
        self.texture = None
        self.frame_rec = None

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\hay.png")
        self.frame_rec = Rectangle(0, 0, self.texture.width, self.texture.height)

    def update(self):
        pass

    def draw(self):
        draw_texture_pro(self.texture, self.frame_rec, self.rect, Vector2(0,0), 0, WHITE)

    def shutdown(self):
        unload_texture(self.texture)