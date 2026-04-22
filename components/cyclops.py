from pyray import *
from settings import *
from enums import Tiles, CyclopsState
from components.healthbar import HealthBar

class Cyclops:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE * 0.7
        self.height = TILE_SIZE * 0.7
        self.rect = Rectangle(x, y, self.width, self.height)
        self.state = CyclopsState.WALKING
        
        # Physics/Movement
        self.vx = ENEMY_SPEED # Start moving right
        self.vy = 0.0 
        self.is_grounded = False

        self.health = 100
        self.health_bar = HealthBar(self.health, x, y-10, self.width, 5)

    def get_rect(self):
        """Returns the enemy's collision bounding box."""
        return self.rect

    def update(self, delta_time, level):
        # 1. Apply Gravity

        match self.state:
            case CyclopsState.WALKING:
                if self.is_grounded:
                    self.vy = 0.0
                self.vy += GRAVITY_ENTITY * delta_time
                self.is_grounded = False 

                self.rect.x += self.vx * delta_time
                self.handle_tile_collision(level, 'X')
                
                self.rect.y += self.vy * delta_time
                self.handle_tile_collision(level, 'Y')
            case CyclopsState.DEAD:
                self.vx = 0
                self.vy = 0
            

        self.health_bar.update(self.rect.x, self.rect.y - 20)
        self.health_bar.update_health(self.health)

        if self.health <= 0:
            self.state = CyclopsState.DEAD

    def handle_tile_collision(self, level, axis):
        """Enemy collision: reverses direction on horizontal wall contact, respects vertical floor contact."""
        enemy_rect = self.get_rect()
        px, py, pw, ph = enemy_rect.x, enemy_rect.y, enemy_rect.width, enemy_rect.height
        
        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue
                
                if level[row][col] == Tiles.SOLID or level[row][col] == Tiles.BOUNDARY:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if check_collision_recs(enemy_rect, tile_rect):
                        
                        if axis == 'X':
                            # Reverses direction on horizontal collision
                            if self.vx > 0:
                                self.rect.x = tile_rect[0] - self.rect.width
                            elif self.vx < 0:
                                self.rect.x = tile_rect[0] + TILE_SIZE
                            self.vx *= -1 # Reverse direction
                            
                        elif axis == 'Y':
                            if self.vy >= 0: # Hitting Ground
                                self.rect.y = tile_rect[1] - self.rect.height
                                self.is_grounded = True 
                                
                            self.vy = 0.0 
                            
                        enemy_rect = self.get_rect() # Update rect after resolution

    def draw(self):

        # Draw a small indicator for state for debugging
        center_x = int(self.rect.x + self.rect.width / 2)
        center_y = int(self.rect.y + self.rect.height / 2)


        match self.state:
            case CyclopsState.WALKING:
                draw_rectangle(int(self.rect.x), int(self.rect.y), int(self.rect.width), int(self.rect.height), RED)
                draw_rectangle_lines(int(self.rect.x), int(self.rect.y), int(self.rect.width), int(self.rect.height), BLACK)
                self.health_bar.draw()
                draw_text("W", center_x, center_y, 10, BLACK)
            case CyclopsState.ANGRY:
                draw_text("A", center_x, center_y, 10, BLACK)
                draw_rectangle(int(self.rect.x), int(self.rect.y), int(self.rect.width), int(self.rect.height), RED)
                draw_rectangle_lines(int(self.rect.x), int(self.rect.y), int(self.rect.width), int(self.rect.height), BLACK)
                self.health_bar.draw()
            case CyclopsState.DEAD:
                pass


