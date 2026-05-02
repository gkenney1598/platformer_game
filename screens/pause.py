from pyray import *
from settings import *

class Pause_Screen:
    def __init__(self):
        self.pause = None
        self.pause_src = None
        self.pause_dest = None
        self.text = "Press ENTER to start"
        self.instructions_text = "Press I for instructions"

    def startup(self):
        self.pause = load_texture(str(THIS_DIR) + "\\resources\\pause.png")
        self.pause_src = Rectangle(0, 0, self.pause.width, self.pause.height)
        self.pause_dest = Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def update(self, delta_time):
        pass

    def draw(self):
        draw_texture_pro(self.pause, self.pause_src, self.pause_dest, Vector2(0,0), 0, WHITE)
        draw_text(self.text, 315, 350, 30, YELLOW)
        draw_text(self.instructions_text, 305, 390, 30, YELLOW)

    def shutdown(self):
        unload_texture(self.pause)