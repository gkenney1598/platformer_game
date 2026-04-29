from pyray import *
from settings import *

class Hay:
    def __init__(self):
        self.texture = None
        self.frame_rec = None
        self.collection = []

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\hay.png")
        self.frame_rec = Rectangle(0, 0, self.texture.width, self.texture.height)

    def draw(self):
        for hay in self.collection:
            draw_texture_pro(self.texture, self.frame_rec, hay, Vector2(0,0), 0, WHITE)

    def shutdown(self):
        unload_texture(self.texture)