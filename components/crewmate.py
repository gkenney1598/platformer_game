from pyray import *
from settings import *
from enums import Axis, Tiles, AnimationType, Direction, SheepState
from utils.anim import Animation

class CrewMates:
    def __init__(self):
        self.collection = []
        self.texture = None
        self.texture_rec = None
        self.mate_count_rect = Rectangle(0, TILE_SIZE, TILE_SIZE * 0.7, TILE_SIZE * 0.8)
        self.total_collected = 0
    
    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\crewmate.png")
        self.texture_rec = Rectangle(0, 0, self.texture.width, self.texture.height)
    
    def update(self, game_level, delta_time):
        for mate in self.collection:
            if not mate.is_collected:
                mate.update(delta_time, game_level, self.texture_rec)
    
    def draw(self):
        for mate in self.collection:
            if not mate.is_collected:
                draw_texture_pro(self.texture, self.texture_rec, mate.rect, Vector2(0,0), 0, WHITE)
                
    def shutdown(self):
        unload_texture(self.texture)

    def draw_mate_count(self):
        for i in range(self.total_collected):
            self.mate_count_rect.x = 30 * i
            draw_texture_pro(self.texture, self.texture_rec, self.mate_count_rect, Vector2(0,0), 0, WHITE)

class CrewMate:
    def __init__(self, x, y):
        self.rect = Rectangle(x, y, TILE_SIZE, TILE_SIZE)
        self.vx = get_random_value(25, 50)
        self.vy = 0.0 
        self.is_grounded = True
        self.is_collected = False

        self.direction = Direction.RIGHT
    

    def update(self, delta_time, level, texture_rec):

        if self.is_grounded:
            self.vy = 0.0
        self.vy += GRAVITY_ENTITY * delta_time
        self.is_grounded = False 

        self.rect.x += self.vx * delta_time
        self.handle_tile_collision(level, Axis.X_AXIS)
        
        self.rect.y += self.vy * delta_time
        self.handle_tile_collision(level, Axis.Y_AXIS)

    def handle_tile_collision(self, level, axis):        
        min_col = int(self.rect.x / TILE_SIZE)
        max_col = int((self.rect.x + self.rect.width) / TILE_SIZE)
        min_row = int(self.rect.y / TILE_SIZE)
        max_row = int((self.rect.y + self.rect.height) / TILE_SIZE)


        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue
                if level[row][col] == Tiles.SOLID or level[row][col] == Tiles.BOUNDARY:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if check_collision_recs(self.rect, tile_rect):
                        match axis:
                            case Axis.X_AXIS:
                                if self.vx > 0:
                                    self.rect.x = tile_rect[0] - self.rect.width
                                elif self.vx < 0:
                                    self.rect.x = tile_rect[0] + TILE_SIZE
                                self.vx *= -1 
                            
                            case Axis.Y_AXIS:
                                if self.vy >= 0: 
                                    self.rect.y = tile_rect[1] - self.rect.height
                                    self.is_grounded = True 
                                
                                self.vy = 0.0 