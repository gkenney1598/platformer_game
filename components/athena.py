from pyray import *
from settings import *
from utils.anim import Animation
from enums import AnimationType

class Athena:
    def __init__(self, x, y):
        self.rect = Rectangle(x - TILE_SIZE * 1.5, y - TILE_SIZE * 2, TILE_SIZE * 4, TILE_SIZE * 3)
        self.texture = None

        self.time = 0
        self.timer = 5
        self.shown = False

        self.anim = Animation(first=0, last=2, cur=0, step=1, 
                              duration=0.2, duration_left=0.2, 
                              anim_type=AnimationType.REPEATING,
                            row=0, sprites_in_row=3)
        
    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\athena.png")

    def update(self, delta_time):
        self.time += delta_time
        if self.time >= self.timer:
            self.shown = False
        self.anim.update(delta_time)

    def draw(self):
        frame = self.anim.frame(self.texture.width / 3, 0)
        frame.width *= -1
        draw_texture_pro(self.texture, frame, self.rect, Vector2(0, 0), 0, WHITE)
    
    def shutdown(self):
        unload_texture(self.texture)
