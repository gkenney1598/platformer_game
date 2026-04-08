from pyray import *
from settings import *
from utils.anim import Animation, AnimationType

class Coin:
    def __init__(self):
        self.texture = None
        self.frame_rec = None
        self.texture_timer = 0
        self.texture_switch = 1 / (TILE_SIZE / 6)
        self.animation = Animation(
            first=0, last=5, cur=0,
            step=1, duration=0.1, duration_left=0.1,
            anim_type=AnimationType.REPEATING,
            row=0, sprites_in_row=6)
        
    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "/resources/coin.png")
        # self.frame_rec = Rectangle(0.0, 0.0, float(self.texture.width)/COIN_FRAMES, float(self.texture.height))

    def update(self):
        dt = get_frame_time()
        self.animation.update(dt)

    def draw(self, coins):
        # radius = TILE_SIZE * 0.3 / 2 
    
        # for cx, cy in coins:
        #     v1 = Vector2(cx, cy - radius * 2)
        #     v2 = Vector2(cx + radius * 1.5, cy)
        #     v3 = Vector2(cx, cy + radius * 2)
        #     v4 = Vector2(cx - radius * 1.5, cy)
            
        #     draw_triangle(v1, v2, v4, YELLOW)
        #     draw_triangle(v2, v3, v4, GOLD)
            
        #     draw_line_v(v1, v3, BLACK)
        #     draw_line_v(v2, v4, BLACK)
        for x, y in coins:
            draw_texture_pro(self.texture, self.animation.frame(self.texture.width/6, 0), Rectangle(x, y, 50, 50), Vector2(0, 0), 0, SKYBLUE)

    def shutdown(self):
        unload_texture(self.texture)