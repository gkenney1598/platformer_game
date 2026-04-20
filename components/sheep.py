from pyray import *
from settings import *
from enums import Axis, Tiles

class Sheep:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE * 0.7, TILE_SIZE * 0.7)
        
        # Physics/Movement
        self.vx = ENEMY_SPEED # Start moving right
        self.vy = 0.0 
        self.is_grounded = True
        self.is_friendly = False
        self.hay = 0
        self.is_held = False
    
    def startup(self):
        pass

    def update(self, delta_time, level):
        # 1. Apply Gravity
        if self.is_grounded:
            self.vy = 0.0
        self.vy += GRAVITY_ENTITY * delta_time
        self.is_grounded = False 

        if not self.is_held:
            self.rect.x += self.vx * delta_time
            self.handle_tile_collision(level, Axis.X_AXIS)
            
            self.rect.y += self.vy * delta_time
            self.handle_tile_collision(level, Axis.Y_AXIS)

        if not self.is_friendly and self.hay >= 1:
            self.is_friendly = True

    def move_with_player(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def handle_tile_collision(self, level, axis):
        """Enemy collision: reverses direction on horizontal wall contact, respects vertical floor contact."""
        sheep_rect = self.rect
        px, py, pw, ph = sheep_rect.x, sheep_rect.y, sheep_rect.width, sheep_rect.height

        
        min_col = int(px / TILE_SIZE)
        max_col = int((px + pw) / TILE_SIZE)
        min_row = int(py / TILE_SIZE)
        max_row = int((py + ph) / TILE_SIZE)


        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue

                if level[row][col] == Tiles.SOLID:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if check_collision_recs(sheep_rect, tile_rect):
                        match axis:
                            case Axis.X_AXIS:
                                # Reverses direction on horizontal collision
                                if self.vx > 0:
                                    self.rect.x = tile_rect[0] - self.rect.width
                                elif self.vx < 0:
                                    self.rect.x = tile_rect[0] + TILE_SIZE
                                self.vx *= -1 # Reverse direction
                            
                            case Axis.Y_AXIS:
                                if self.vy >= 0: # Hitting Ground
                                    self.rect.y = tile_rect[1] - self.rect.height
                                    self.is_grounded = True 
                                
                                self.vy = 0.0 
                            
                        sheep_rect = self.rect# Update rect after resolution
    
    def draw(self):
        """Draws the enemy as a red rectangle with a directional indicator."""
        draw_rectangle_rec(self.rect, RAYWHITE)
        draw_rectangle_lines_ex(self.rect, 2, BLACK)
        
        # Draw a small indicator for direction
        center_x = int(self.rect.x + self.rect.width / 2)
        center_y = int(self.rect.y + self.rect.height / 2)
        # indicator_size = self.rect.width * 0.2

        if self.is_friendly:
            draw_text("F", center_x, center_y, 10, BLACK)
        else:
            draw_text("UF", center_x, center_y, 10, BLACK)
            
    def shutdown(self):
        pass