from pyray import *
from settings import *

class Gold:
    def __init__(self):
        self.texture = None
        self.frame_rec = None
        self.collection = []
        self.gold_count = Rectangle(5, 5, TILE_SIZE * 0.7, TILE_SIZE * 0.4)

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\gold.png")
        self.frame_rec = Rectangle(0, 0, self.texture.width, self.texture.height)


    def draw(self):
        for gold in self.collection:
            draw_texture_pro(self.texture, self.frame_rec, gold, Vector2(0,0), 0, WHITE)
    
    def draw_gold_count(self, player_gold):
        for i in range(player_gold):
            self.gold_count.x = 30 * i
            draw_texture_pro(self.texture, self.frame_rec, self.gold_count, Vector2(0,0), 0, WHITE)

    def shutdown(self):
        unload_texture(self.texture)