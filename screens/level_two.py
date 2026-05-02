from pyray import *
from settings import *
from utils.level import Level

class Level_Two:
    def __init__(self):
        self.level, self.solid = Level.parse_level_two(LEVEL_TWO)

    def startup(self):
        self.solid.startup()
    
    def update(self, player, delta_time, camera):
        player.update(delta_time, self.level)
        camera.update(player)
    
    def draw(self, player, camera):
        begin_mode_2d(camera.camera)

        player.draw()
        self.solid.draw()

        end_mode_2d()
    
    def shutdown(self):
        self.solid.shutdown()
