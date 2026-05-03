from pyray import *
from settings import *
from enums import Tiles, CyclopsState, Direction, AnimationType
from utils.anim import Animation
from components.healthbar import HealthBar

class Cyclopses:
    def __init__(self):
        self.collection = []
        self.texture = None
    
    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\\cyclops.png")

    def update(self, game_level, player, delta_time):
        for cyclops in self.collection:
            cyclops.update(delta_time, game_level, player.rect)
            if not player.is_sheep:
                cyclops.check_player_nearby(player.attention_box)

    def draw(self):
        for cyclops in self.collection:
            cyclops.draw(self.texture)
    
    def shutdown(self):
        unload_texture(self.texture)

class Cyclops:
    def __init__(self, x, y, width=TILE_SIZE * 2, height=TILE_SIZE * 2.5, boss=False):
        self.x = x
        self.y = y
        self.rect = Rectangle(x, y, width, height)
        self.bounding_box = Rectangle(x, y, TILE_SIZE * 2, TILE_SIZE * 2)
        self.state = CyclopsState.WALKING
        
        self.vx = ENEMY_SPEED
        self.vy = 0.0 
        self.is_grounded = False

        self.health = 100
        self.health_bar = HealthBar(self.health, x, y, self.rect.width / 2, 5)

        self.angry_time = 2
        self.angry_timer = 0

        self.attack_cooldown = 0.75
        self.attack_timer = 0

        self.boss = boss

        self.moving = True
        self.direction = Direction.RIGHT
        self.walk = Animation(first=0, last=11, cur=0, step=1, 
                              duration=0.2, duration_left=0.2, 
                              anim_type=AnimationType.REPEATING,
                            row=1, sprites_in_row=12)
        self.angry = Animation(first=0, last=6, cur=0, step=1, 
                              duration=0.2, duration_left=0.2, 
                              anim_type=AnimationType.REPEATING,
                            row=2, sprites_in_row=7)
        self.attack_anim = Animation(first=0, last=12, cur=0, step=1, 
                              duration=0.05, duration_left=0.05, 
                              anim_type=AnimationType.ONESHOT,
                            row=3, sprites_in_row=13)
        self.dead = Animation(first=0, last=8, cur=0, step=1, 
                              duration=0.4, duration_left=0.4, 
                              anim_type=AnimationType.ONESHOT,
                            row=6, sprites_in_row=9) 

    def update(self, delta_time, level, player_rect):
        match self.state:
            case CyclopsState.WALKING:
                if self.is_grounded:
                    self.vy = 0.0
                self.vy += GRAVITY_ENTITY * delta_time
                self.is_grounded = False 
                self.walk.update(delta_time)

            case CyclopsState.DEAD:
                self.moving = False
                self.dead.update(delta_time)

            case CyclopsState.ANGRY:
                if self.is_grounded:
                    self.vy = 0.0
                self.vy += GRAVITY_ENTITY * delta_time
                self.is_grounded = False 
                self.angry_timer += delta_time
                if player_rect.x < self.rect.x:
                    self.vx = -ENEMY_SPEED
                    self.direction = Direction.LEFT
                else:
                    self.vx = ENEMY_SPEED
                    self.direction = Direction.RIGHT
                self.angry.update(delta_time)

            case CyclopsState.ATTACK:
                self.attack_anim.update(delta_time)
                if self.attack_anim.done:
                    self.state = CyclopsState.ANGRY
                    self.attack_anim.reset()
                    self.moving = True

        if self.moving:         
            self.rect.x += self.vx * delta_time
            self.bounding_box.x += self.vx * delta_time
            self.handle_tile_collision(level, 'X')
            
            self.rect.y += self.vy * delta_time
            self.bounding_box.y += self.vy * delta_time
            self.handle_tile_collision(level, 'Y')

        
        self.health_bar.update(self.rect.x + int(self.rect.width/4), self.rect.y + 20)
        self.health_bar.update_health(self.health) 

        if self.health <= 0:
            self.state = CyclopsState.DEAD

    def attack(self, delta_time):
        if self.attack_timer >= self.attack_cooldown:
            self.state = CyclopsState.ATTACK
            self.moving = False
            self.attack_timer = 0
            return 10
        self.attack_timer += delta_time
        return 0

    def handle_tile_collision(self, level, axis):
        min_col = int(self.bounding_box.x / TILE_SIZE)
        max_col = int((self.bounding_box.x + self.bounding_box.width) / TILE_SIZE)
        min_row = int(self.bounding_box.y / TILE_SIZE)
        max_row = int((self.bounding_box.y + self.bounding_box.height) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue
                
                if level[row][col] == Tiles.SOLID or level[row][col] == Tiles.BOUNDARY:

                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if check_collision_recs(self.bounding_box, tile_rect):
                        if (self.state == CyclopsState.ANGRY and level[row][col] == Tiles.SOLID) or self.state != CyclopsState.ANGRY:                        
                            if axis == 'X':
                                    # Reverses direction on horizontal collision
                                    if self.vx > 0:
                                        self.rect.x = tile_rect[0] - self.rect.width
                                        self.bounding_box.x = tile_rect[0] - self.bounding_box.width
                                    elif self.vx < 0:
                                        self.rect.x = tile_rect[0] + TILE_SIZE
                                        self.bounding_box.x = tile_rect[0] + TILE_SIZE
                                    self.vx *= -1 # Reverse direction
                                    self.direction = Direction.RIGHT if self.vx > 0 else Direction.LEFT
                                
                            elif axis == 'Y':
                                if self.vy >= 0: # Hitting Ground
                                    self.rect.y = tile_rect[1] - self.rect.height
                                    self.bounding_box.y = tile_rect[1] - self.bounding_box.height
                                    self.is_grounded = True 
                                    
                                self.vy = 0.0 
                        

    def check_player_nearby(self, player_attention_box):
        match self.state:
            case CyclopsState.WALKING:
                if check_collision_recs(self.rect, player_attention_box):
                    self.state = CyclopsState.ANGRY

            case CyclopsState.ANGRY:
                if not check_collision_recs(self.rect, player_attention_box) and self.angry_timer >= self.angry_time:
                    self.state = CyclopsState.WALKING
                    self.angry_timer = 0

    def draw(self, texture):
        match self.state:
            case CyclopsState.WALKING:
                frame = self.walk.frame(texture.width / 15, 1)
                frame.width *= self.direction
                draw_texture_pro(texture, frame, self.rect, Vector2(0, 0), 0, WHITE)

            case CyclopsState.ANGRY:
                frame = self.angry.frame(texture.width / 15, 2)
                frame.width *= self.direction
                draw_texture_pro(texture, frame, self.rect, Vector2(0, 0), 0, WHITE)

            case CyclopsState.DEAD:
                frame = self.dead.frame(texture.width / 15, 6)
                draw_texture_pro(texture, frame, self.rect, Vector2(0,0), 0, WHITE)

            case CyclopsState.ATTACK:
                frame = self.attack_anim.frame(texture.width / 15, 3)
                frame.width *= self.direction
                draw_texture_pro(texture, frame, self.rect, Vector2(0, 0), 0, WHITE)

        if self.state != CyclopsState.DEAD and not self.dead.done:
            self.health_bar.draw()