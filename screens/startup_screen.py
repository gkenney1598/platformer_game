from pyray import *
from settings import *
from enums import Direction

class Startup_Screen:
    def __init__(self):
        self.insturctions = "Press ENTER to start"

        self.ship_texture = None
        self.ship_dest = Rectangle(150, 425, 300, 300)
        self.ship_src = None
        self.ship_origin = None

        self.ship_rotation = 0
        self.rotation_time = 0
        self.rotation_timer = 0.5
        self.max_rotation = 5
        self.rotation_direction = Direction.RIGHT

        self.ocean_background = None
        self.background_dest = (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background_src = None

        self.title = None
        self.title_dest = None
        self.title_src = None

    def startup(self):
        self.ship_texture = load_texture(str(THIS_DIR) + "\\resources\\screens\\ship.png")
        self.ship_src = Rectangle(0, 0, self.ship_texture.width, self.ship_texture.height)
        self.ship_origin = Vector2(100, 100)

        self.ocean_background = load_texture(str(THIS_DIR) + "\\resources\\screens\\ocean.png")
        self.background_src = Rectangle(0, 0, self.ocean_background.width, self.ocean_background.height)

        self.title = load_texture(str(THIS_DIR) + "\\resources\\screens\\title_splash.png")
        self.title_src = Rectangle(0, 0, self.title.width, self.title.height)
        self.title_dest = Rectangle(200, 100, self.title.width, self.title.height)

    def update(self, delta_time):
        self.rotation_time += delta_time

        if self.rotation_time > self.rotation_timer:
            match self.rotation_direction:
                case Direction.RIGHT:
                    self.ship_rotation += 0.5
                case Direction.LEFT:
                    self.ship_rotation -= 0.5
            if self.ship_rotation > self.max_rotation or self.ship_rotation < -self.max_rotation:
                self.rotation_direction *= -1
            self.rotation_time = 0

    def draw(self):
        draw_texture_pro(self.ocean_background, self.background_src, self.background_dest, Vector2(0,0), 0, WHITE)
        draw_texture_pro(self.ship_texture, self.ship_src, self.ship_dest, self.ship_origin, self.ship_rotation, WHITE)
        draw_texture_pro(self.title, self.title_src, self.title_dest, Vector2(0,0), 0, WHITE)
        draw_text(self.insturctions, 350, 300, 30, YELLOW)
        

    def shutdown(self):
        unload_texture(self.ship_texture)
        unload_texture(self.ocean_background)