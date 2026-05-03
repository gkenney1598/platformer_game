from pyray import *
from settings import *

class Win_Screen:
    def __init__(self):
        self.pause = None
        self.pause_src = None
        self.pause_dest = None
        self.text = "Press ENTER to start"

    def startup(self):
        self.pause = load_texture(str(THIS_DIR) + "\\resources\\win.png")
        self.pause_src = Rectangle(0, 0, self.pause.width, self.pause.height)
        self.pause_dest = Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def update(self, delta_time):
        pass

    def draw(self):
        draw_texture_pro(self.pause, self.pause_src, self.pause_dest, Vector2(0,0), 0, WHITE)
        draw_text(self.text, 315, 350, 30, YELLOW)

    def shutdown(self):
        unload_texture(self.pause)