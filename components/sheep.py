from pyray import *
from settings import *
from enums import Axis, Tiles, AnimationType, Direction
from utils.anim import Animation

class Sheep:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
        # Physics/Movement
        self.vx = get_random_value(25, 50)
        self.vy = 0.0 
        self.is_grounded = True
        self.is_friendly = False #TODO: add sheep states
        self.hay = 0
        self.is_held = False
        self.walking_y = y
        self.texture = None
        self.width = None
        self.height = None

        cur = get_random_value(0, 18)
        self.idle = Animation(first=0, last=18, cur=cur, 
                              step=1, duration=0.3, duration_left=0.3, 
                              anim_type=AnimationType.REPEATING, 
                              row=1, sprites_in_row=19)
        self.direction = Direction.RIGHT
    
    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\sheep.png")
        self.width = self.texture.width / self.idle.sprites_in_row
        self.height = self.texture.height / 3

    def update(self, delta_time, level):
        # 1. Apply Gravity
        if self.is_grounded:
            self.vy = 0.0
        self.vy += GRAVITY_ENTITY * delta_time
        self.is_grounded = False 

        if not self.is_held and (self.idle.cur < 11 or self.idle.cur > 17):
            self.rect.x += self.vx * delta_time
            self.handle_tile_collision(level, Axis.X_AXIS)
            
            self.rect.y += self.vy * delta_time
            self.handle_tile_collision(level, Axis.Y_AXIS)

        if not self.is_friendly and self.hay >= 1:
            self.is_friendly = True

        self.idle.update(delta_time)

    def move_with_player(self, x, y):
        self.rect.x = x + 20
        self.rect.y = y + 10

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
                if level[row][col] == Tiles.SOLID or level[row][col] == Tiles.BOUNDARY:
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
                                self.direction = Direction.RIGHT if self.vx > 0 else Direction.LEFT
                            
                            case Axis.Y_AXIS:
                                if self.vy >= 0: # Hitting Ground
                                    self.rect.y = tile_rect[1] - self.rect.height
                                    self.is_grounded = True 
                                
                                self.vy = 0.0 
                            
                        sheep_rect = self.rect# Update rect after resolution
    
    def draw(self):
        """Draws the enemy as a red rectangle with a directional indicator."""
        frame = self.idle.frame(self.width, 1)
        frame.width *= self.direction
        draw_texture_pro(self.texture, frame, self.rect, Vector2(0,0), 0, WHITE)
        
            
    def shutdown(self):
        unload_texture(self.texture)