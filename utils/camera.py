from pyray import *
from settings import *


class Camera():
    def __init__(self, player_rect):
        self.camera = Camera2D()
        self.camera.target = Vector2(player_rect.x, player_rect.y) 
        self.camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0
    
    def update(self, player):
        self.camera.target.x = player.rect.x + player.rect.width / 2
        self.camera.target.y = player.rect.y + player.rect.height / 2

        min_x = SCREEN_WIDTH / 2
        max_x = WORLD_WIDTH - SCREEN_WIDTH / 2
        
        if self.camera.target.x < min_x:
            self.camera.target.x = min_x
        if self.camera.target.x > max_x:
            self.camera.target.x = max_x

        min_y = SCREEN_HEIGHT / 2
        max_y = WORLD_HEIGHT - SCREEN_HEIGHT / 2
        
        if self.camera.target.y < min_y:
            self.camera.target.y = min_y
        if self.camera.target.y > max_y:
            self.camera.target.y = max_y
        
        self.camera.offset.x = SCREEN_WIDTH / 2
        self.camera.offset.y = SCREEN_HEIGHT / 2
