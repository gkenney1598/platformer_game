from pyray import *
from settings import *

class Hay:
    def __init__(self):
        self.texture = None
        self.frame_rec = None
        self.collection = []
        self.hay_count = None
        self.hay_count = Rectangle(5, -10, TILE_SIZE * 0.7, TILE_SIZE * 0.4)

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\hay.png")
        self.frame_rec = Rectangle(0, 0, self.texture.width, self.texture.height)


    def draw(self, player_hay):
        for hay in self.collection:
            draw_texture_pro(self.texture, self.frame_rec, hay, Vector2(0,0), 0, WHITE)
        for i in range(player_hay):
            self.hay_count.x = 30 * i
            draw_texture_pro(self.texture, self.frame_rec, self.hay_count, Vector2(0,0), 0, WHITE)

    def shutdown(self):
        unload_texture(self.texture)