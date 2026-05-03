from pyray import *
from settings import *
from enums import GameState


class Camera():
    def __init__(self, target, offset, zoom):
        self.camera = Camera2D()
        self.camera.target = target 
        self.camera.offset = offset
        self.camera.rotation = 0.0
        self.camera.zoom = zoom
    
    def update(self, player, level, mini = False):
        match level:
            case GameState.LEVEL_ONE:
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


            case GameState.LEVEL_TWO:
                bounding_box = Vector2(0.2, 0.2)

                screen_min = Vector2((1 - bounding_box.x) * 0.5 * SCREEN_WIDTH - 400, (1 - bounding_box.y) * 0.5 * SCREEN_HEIGHT - 100)
                screen_max = Vector2((1 + bounding_box.x) * 0.5 * SCREEN_WIDTH + 200, (1 + bounding_box.y) * 0.5 * SCREEN_HEIGHT + 75)

                if mini:
                    screen_max = Vector2((1 + bounding_box.x) * 0.5 * SCREEN_WIDTH + 200, (1 + bounding_box.y) * 0.5 * SCREEN_HEIGHT + 245)

                bbox_world_min = get_screen_to_world_2d(screen_min, self.camera)
                bbox_world_max = get_screen_to_world_2d(screen_max, self.camera)

                self.camera.offset = screen_min

                if mini:
                    self.camera.target.x = player.rect.x - 200
                elif player.rect.x < bbox_world_min.x or mini:
                    self.camera.target.x = player.rect.x
                elif player.rect.x > bbox_world_max.x:
                    self.camera.target.x = bbox_world_min.x + (player.rect.x - bbox_world_max.x)
                    
                if player.rect.y > bbox_world_max.y or mini:
                    self.camera.target.y = bbox_world_min.y + (player.rect.y - bbox_world_max.y)
                elif player.rect.y < bbox_world_min.y:
                    self.camera.target.y = player.rect.y


        
