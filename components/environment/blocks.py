from pyray import *
from settings import TILE_SIZE, THIS_DIR, CAVE_TILE_SIZE

class Blocks:
    def __init__(self):
        self.collection = []

        self.grass_texture = None
        self.grass_frame_rec = None

        self.pillar_texture = None     
        self.pillar_frame_rec = None

        self.cave_texture = None
        self.cave_grass_frame_rec = None

        self.stone_frame_rec = None
    
    def append(self, block):
        self.collection.append(block)
    
    def startup(self, texture=None):
        self.grass_texture = load_texture(str(THIS_DIR) + "\\resources\\level_one\\grass.png")
        self.grass_frame_rec = Rectangle(0, 0, self.grass_texture.width, self.grass_texture.height)

        self.pillar_texture = load_texture(str(THIS_DIR) + "\\resources\\level_one\\pillar.png")
        self.pillar_frame_rec = Rectangle(0, 0, self.pillar_texture.width, self.pillar_texture.height)

        self.cave_grass_frame_rec = Rectangle(0, CAVE_TILE_SIZE * 2, CAVE_TILE_SIZE, CAVE_TILE_SIZE)
        self.stone_frame_rec= Rectangle(0, CAVE_TILE_SIZE, CAVE_TILE_SIZE, CAVE_TILE_SIZE)

        self.cave_texture = texture


    def draw(self):
        for block in self.collection:
            if isinstance(block, Grass):
                draw_texture_pro(self.grass_texture, self.grass_frame_rec, block.rect, Vector2(0, 0), 0.0, WHITE)

            elif isinstance(block, Pillar):
                draw_texture_pro(self.pillar_texture, self.pillar_frame_rec, block.rect, Vector2(0, 0), 0.0, WHITE)

            elif isinstance(block, Cave_Grass):
                draw_texture_pro(self.cave_texture, self.cave_grass_frame_rec, block.rect, Vector2(0, 0), 0.0, WHITE)
                
            elif isinstance(block, Stone):
                draw_texture_pro(self.cave_texture, self.stone_frame_rec, block.rect, Vector2(0, 0), 0.0, WHITE)
    
    def shutdown(self):
        unload_texture(self.grass_texture)
        unload_texture(self.pillar_texture)

class Grass: 
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)

class Pillar:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)

class Cave_Grass:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)

class Stone:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)

