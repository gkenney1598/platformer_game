from pyray import *
from settings import *

class Hay:
    def __init__(self):
        self.texture = None
        self.frame_rec = None
        self.collection = []
        self.hay_count = None
        self.hay_rect = Rectangle(5, 5, TILE_SIZE * 0.7, TILE_SIZE * 0.4)

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\hay.png")
        self.frame_rec = Rectangle(0, 0, self.texture.width, self.texture.height)


    def draw(self):
        for hay in self.collection:
            draw_texture_pro(self.texture, self.frame_rec, hay, Vector2(0,0), 0, WHITE)
    
    def draw_hay_count(self, player_hay):
        for i in range(player_hay):
            self.hay_count.x = 30 * i
            draw_texture_pro(self.texture, self.frame_rec, self.hay_rect, Vector2(0,0), 0, WHITE)

    def shutdown(self):
        unload_texture(self.texture)