from pyray import *
from settings import *

class Instruction_Screen:
    def __init__(self):
        self.instructions = None
        self.instructions_src = None
        self.instructions_dest = None
        self.text = "Press ENTER to start"

    def startup(self):
        self.instructions = load_texture(str(THIS_DIR) + "\\resources\\screens\\instruction.png")
        self.instructions_src = Rectangle(0, 0, self.instructions.width, self.instructions.height)
        self.instructions_dest = Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    def update(self, delta_time):
        pass

    def draw(self):
        draw_texture_pro(self.instructions, self.instructions_src, self.instructions_dest, Vector2(0,0), 0, WHITE)
        draw_text(self.text, 325, 150, 30, YELLOW)
        

    def shutdown(self):
        unload_texture(self.instructions)