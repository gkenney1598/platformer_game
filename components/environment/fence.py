from pyray import *
from settings import THIS_DIR, TILE_SIZE

class Fences:
    def __init__(self):
        self.collection = []
        self.texture = None
        self.source_rect = None

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