from pyray import *
from settings import *

class Vases:
    def __init__(self):
        self.texture = None
        self.frame_rec = None
        self.collection = []
    
    def append(self, vase):
        self.collection.append(vase)

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\vase.png")
        self.frame_rec = Rectangle(0, 0, self.texture.width, self.texture.height)

    def draw(self):
        for vase in self.collection:
            draw_texture_pro(self.texture, self.frame_rec, vase.rect, Vector2(0, 0), 0.0, WHITE)

    def shutdown(self):
        unload_texture(self.texture)

class Vase:
    def __init__(self, x, y, full):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
        self.full = full