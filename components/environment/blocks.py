from pyray import *
from settings import TILE_SIZE, THIS_DIR

class Blocks:
    def __init__(self):
        self.collection = []
        self.grass_texture = None
        self.pillar_texture = None
        self.grass_frame_rec = None
        self.pillar_frame_rec = None
    
    def startup(self):
        self.grass_texture = load_texture(str(THIS_DIR) + "\\resources\\grass.png")
        self.grass_frame_rec = Rectangle(0, 0, self.grass_texture.width, self.grass_texture.height)
        self.pillar_texture = load_texture(str(THIS_DIR) + "\\resources\\pillar.png")
        self.pillar_frame_rec = Rectangle(0, 0, self.pillar_texture.width, self.pillar_texture.height)

    def draw(self):
        for block in self.collection:
            if isinstance(block, Grass):
                draw_texture_pro(self.grass_texture, self.grass_frame_rec, block.rect, Vector2(0, 0), 0.0, WHITE)
            elif isinstance(block, Pillar):
                draw_texture_pro(self.pillar_texture, self.pillar_frame_rec, block.rect, Vector2(0, 0), 0.0, WHITE)
    
    def shutdown(self):
        unload_texture(self.grass_texture)
        unload_texture(self.pillar_texture)

class Grass: 
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)

class Pillar:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)

