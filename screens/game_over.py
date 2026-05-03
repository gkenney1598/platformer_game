from pyray import *
from settings import *

class Game_Over:
    def __init__(self):
        self.game_over = None
        self.game_over_src = None
        self.game_over_dest = None
        self.text = "Press ENTER to restart"

    def startup(self):
        self.game_over = load_texture(str(THIS_DIR) + "\\resources\\screens\\game_over.png")
        self.game_over_src = Rectangle(0, 0, self.game_over.width, self.game_over.height)
        self.game_over_dest = Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def draw(self):
        draw_texture_pro(self.game_over, self.game_over_src, self.game_over_dest, Vector2(0,0), 0, WHITE)
        draw_text(self.text, 315, 350, 30, YELLOW)

    def shutdown(self):
        unload_texture(self.game_over)