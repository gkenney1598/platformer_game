from pyray import *
from settings import THIS_DIR, TILE_SIZE, CAVE_TILE_SIZE

class Altar:
    def __init__(self, x, y):
        self.rect_pillar = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
        self.rect_bowl = Rectangle(x, y - TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.texture = None
        self.source_rect_pillar = Rectangle(CAVE_TILE_SIZE * 5, CAVE_TILE_SIZE * 25, CAVE_TILE_SIZE, CAVE_TILE_SIZE)
        self.source_rect_bowl = Rectangle(CAVE_TILE_SIZE * 4, CAVE_TILE_SIZE * 20, CAVE_TILE_SIZE, CAVE_TILE_SIZE)
        self.gold = 0
        self.offer_complete = False

    def startup(self, texture):
        self.texture = texture

    def draw(self):
        draw_texture_pro(self.texture, self.source_rect_pillar, self.rect_pillar, Vector2(0,0), 0, WHITE)
        draw_texture_pro(self.texture, self.source_rect_bowl, self.rect_bowl, Vector2(0,0), 0, WHITE)
   
    def shutdown(self):
        pass