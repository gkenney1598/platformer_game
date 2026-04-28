from pyray import *
from settings import TILE_SIZE, THIS_DIR

class Grass: 
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
        self.texture = None
        self.frame_rec = None

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\grass.png")
        self.frame_rec = Rectangle(0, 0, self.texture.width, self.texture.height)

    def draw(self):
        draw_texture_pro(self.texture, self.frame_rec, self.rect, Vector2(0, 0), 0.0, WHITE)

    def shutdown(self):
        unload_texture(self.texture)

class Pillar:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
        self.texture = None
        self.frame_rec = None

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\pillar.png")
        self.frame_rec = Rectangle(0, 0, self.texture.width, self.texture.height)

    def draw(self):
        draw_texture_pro(self.texture, self.frame_rec, self.rect, Vector2(0, 0), 0.0, WHITE)

    def shutdown(self):
        unload_texture(self.texture)

