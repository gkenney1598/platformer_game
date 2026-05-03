from pyray import *
from settings import THIS_DIR, TILE_SIZE, CAVE_TILE_SIZE

class Altar:
    def __init__(self, x, y):
        self.texture = None

        self.rect_pillar = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
        self.rect_bowl = Rectangle(x, y - TILE_SIZE, TILE_SIZE, TILE_SIZE)
        
        self.source_rect_pillar = Rectangle(CAVE_TILE_SIZE * 5, CAVE_TILE_SIZE * 25, CAVE_TILE_SIZE, CAVE_TILE_SIZE)
        self.source_rect_bowl = Rectangle(CAVE_TILE_SIZE * 4, CAVE_TILE_SIZE * 20, CAVE_TILE_SIZE, CAVE_TILE_SIZE)
        
        self.gold = 0
        self.offer_complete = False

    def startup(self, texture):
        self.texture = texture

    def draw(self):
        draw_texture_pro(self.texture, self.source_rect_pillar, self.rect_pillar, Vector2(0,0), 0, WHITE)
        draw_texture_pro(self.texture, self.source_rect_bowl, self.rect_bowl, Vector2(0,0), 0, WHITE)

class Door:
    def __init__(self, x, y):
        self.rect_door = Rectangle(x - TILE_SIZE, y - TILE_SIZE * 2, TILE_SIZE * 2, TILE_SIZE * 4)
        self.rect_arch = Rectangle(x + TILE_SIZE, y - TILE_SIZE * 2, TILE_SIZE * 2, TILE_SIZE * 2)
        self.texture = None
        self.source_rect_open = Rectangle(CAVE_TILE_SIZE * 4, CAVE_TILE_SIZE * 2, CAVE_TILE_SIZE, CAVE_TILE_SIZE * 2)
        self.source_rect_close = Rectangle(CAVE_TILE_SIZE * 4, 0, CAVE_TILE_SIZE, CAVE_TILE_SIZE * 2)
        self.source_rect_arch = Rectangle(CAVE_TILE_SIZE * 8, CAVE_TILE_SIZE * 12, CAVE_TILE_SIZE, CAVE_TILE_SIZE)
        self.locked = True
        self.open = False

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\.\\resources\\level_two\\cave.png")

    def draw(self):

        draw_texture_pro(self.texture, self.source_rect_arch, self.rect_arch, Vector2(0,0), 180, WHITE)

        if self.locked:
            draw_texture_pro(self.texture, self.source_rect_close, self.rect_door, Vector2(0,0), 0, WHITE)
        else:
            draw_texture_pro(self.texture, self.source_rect_open, self.rect_door, Vector2(0,0), 0, WHITE)
    
    def shutdown(self):
        unload_texture(self.texture)

class Fences:
    def __init__(self):
        self.collection = []
        self.texture = None
        self.source_rect = None

    def append(self, fence):
        self.collection.append(fence)

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\.\\resources\\level_one\\fence.png")
        self.source_rect = Rectangle(0, 0, self.texture.width, self.texture.height)
    
    def draw(self):
        for fence in self.collection:
            draw_texture_pro(self.texture, self.source_rect, fence.rect, Vector2(0,0), 0, WHITE)

    def shutdown(self):
        unload_texture(self.texture)
        

class Fence:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)