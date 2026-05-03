from pyray import *
from settings import THIS_DIR, TILE_SIZE, CAVE_TILE_SIZE

class Door:
    def __init__(self, x, y):
        self.rect_door = Rectangle(x - TILE_SIZE, y - TILE_SIZE * 2, TILE_SIZE * 2, TILE_SIZE * 4)
        self.rect_arch = Rectangle(x + TILE_SIZE, y - TILE_SIZE * 2, TILE_SIZE * 2, TILE_SIZE * 2)
        self.texture = None
        self.source_rect_open = Rectangle(CAVE_TILE_SIZE * 4, CAVE_TILE_SIZE * 2, CAVE_TILE_SIZE, CAVE_TILE_SIZE * 2)
        self.source_rect_close = Rectangle(CAVE_TILE_SIZE * 4, 0, CAVE_TILE_SIZE, CAVE_TILE_SIZE * 2)
        self.source_rect_arch = Rectangle(CAVE_TILE_SIZE * 8, CAVE_TILE_SIZE * 12, CAVE_TILE_SIZE, CAVE_TILE_SIZE)
        self.locked = False

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\.\\resources\\cave.png")

    def draw(self):

        draw_texture_pro(self.texture, self.source_rect_arch, self.rect_arch, Vector2(0,0), 180, WHITE)

        if self.locked:
            draw_texture_pro(self.texture, self.source_rect_close, self.rect_door, Vector2(0,0), 0, WHITE)
        else:
            draw_texture_pro(self.texture, self.source_rect_open, self.rect_door, Vector2(0,0), 0, WHITE)
    
    def shutdown(self):
        unload_texture(self.texture)
