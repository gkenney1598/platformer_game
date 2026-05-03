from pyray import *
from settings import *
from enums import Tiles, PlayerState, AnimationType, Direction
from components.healthbar import HealthBar
from utils.anim import Animation

#TODO: refactor previous code to use PlayerState
#TODO: debug being able to tranform into sheep while holding a sheep
class Player:
    def __init__(self, x, y):
        self.start_x = x 
        self.start_y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        self.rect = Rectangle(x, y, self.width, self.height)
        self.bounding_box = None
        self.attention_box = Rectangle(x - 200, y - 10, self.width + 400, self.height + 20)

        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False

        self.hay = 0
        self.gold = 0
        self.is_holding = False
        self.state = PlayerState.IDLE
        self.held_object = None
        self.can_transform = False
        self.is_sheep = False
        self.can_special_attack = False

        self.health = 100
        self.health_bar = HealthBar(self.health, (self.rect.x + self.rect.width) / 4, y, self.rect.width, 5)

        #Odysseus texture
        self.texture = None
        self.tile_size = None
        self.player_direction = Direction.RIGHT
        self.idle = Animation(first=0, last=4, cur=0, 
                              step=1, duration=0.3, duration_left=0.3, 
                              anim_type=AnimationType.REPEATING, 
                              row=1, sprites_in_row=5)
        
        self.jump = Animation(first=0, last=6, cur=0,
                              step=1, duration=0.08, duration_left=0.08,
                              anim_type=AnimationType.ONESHOT,
                              row=3, sprites_in_row=7)
        
        self.walk = Animation(first=0, last=8, cur=0,
                                 step=1, duration=0.09, duration_left=0.09,
                                 anim_type=AnimationType.REPEATING,
                                 row=11, sprites_in_row=9)
        self.attack = Animation(first=0, last=7, cur=0,
                                step=1,duration=0.05,duration_left=0.05,
                                anim_type=AnimationType.ONESHOT,
                                row=7, sprites_in_row=8)
        self.dead = Animation(first=0, last=4, cur=0,
                                step=1, duration=0.1, duration_left=0.1,
                                anim_type=AnimationType.ONESHOT,
                                row=20, sprites_in_row=6)
        self.special_attack = Animation(first=0, last=7, cur=0,
                                step=1,duration=0.05,duration_left=0.05,
                                anim_type=AnimationType.ONESHOT,
                                row=5, sprites_in_row=8)
        
        #sheep texture
        self.sheep_texture = None
        self.sheep_idle = Animation(first=0, last=18, cur=0, 
                              step=1, duration=0.3, duration_left=0.3, 
                              anim_type=AnimationType.REPEATING, 
                              row=1, sprites_in_row=19)
        self.sheep_walk =  Animation(first=0, last=4, cur=0, 
                              step=1, duration=0.1, duration_left=0.1, 
                              anim_type=AnimationType.REPEATING, 
                              row=0, sprites_in_row=5)
        self.sheep_bleet = Animation(first=0, last=8, cur=0, 
                              step=1, duration=0.3, duration_left=0.3, 
                              anim_type=AnimationType.ONESHOT, 
                              row=2, sprites_in_row=9)
        
    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\odysseus.png")
        self.width = int(self.texture.width) / 13
        self.rect.width = self.width
        self.height = self.texture.height / 21
        self.rect.height = self.height
        self.bounding_box = Rectangle(self.rect.x + 10, self.rect.y, self.width - 40, self.height)

        self.sheep_texture = load_texture(str(THIS_DIR) + "\\resources\\level_one\\sheep.png")

    def update(self, delta_time, level, held_object = None):

        #Handle User Input
        self.vx = 0.0
        if is_key_down(KeyboardKey.KEY_A):
            self.vx = -PLAYER_SPEED
            self.player_direction = Direction.LEFT
            if self.is_sheep:
                self.state = PlayerState.SHEEP_WALKING
            elif self.state != PlayerState.JUMPING:
                self.state = PlayerState.WALKING

        if is_key_down(KeyboardKey.KEY_D):
            self.vx = PLAYER_SPEED
            self.player_direction = Direction.RIGHT
            if self.is_sheep:
                self.state = PlayerState.SHEEP_WALKING
            elif self.state != PlayerState.JUMPING:
                self.state = PlayerState.WALKING

        if is_key_released(KeyboardKey.KEY_A) or is_key_released(KeyboardKey.KEY_D):
            if self.is_sheep:
                self.state = PlayerState.SHEEP_IDLE
            else:
                self.state = PlayerState.IDLE

        if self.is_grounded:
            self.vy = 0.0
            
        if is_key_pressed(KeyboardKey.KEY_SPACE) and self.is_grounded:
            self.vy = JUMP_VELOCITY
            if not self.is_sheep:
                self.state = PlayerState.JUMPING

        self.vy += GRAVITY_PLAYER * delta_time
        if self.vy > 1000:
            self.vy = 1000

        self.is_grounded = False

        self.rect.x += self.vx * delta_time
        self.attention_box.x = self.rect.x - 200
        self.bounding_box.x = self.rect.x + 20       
        self.handle_tile_collision(level, 'X')
        
        self.rect.y += self.vy * delta_time
        self.attention_box.y = self.rect.y - 10
        self.bounding_box.y = self.rect.y
        self.handle_tile_collision(level, 'Y')

        self.health_bar.update(self.rect.x + self.rect.width / 4, self.rect.y - 5)
        self.health_bar.update_health(self.health)
        
        self.rect.x = max(0, min(self.rect.x, WORLD_WIDTH - self.rect.width))

        if is_key_pressed(KeyboardKey.KEY_T) and self.can_transform:
            self.is_sheep = True
            self.state = PlayerState.SHEEP_IDLE

        if is_key_pressed(KeyboardKey.KEY_Y):
            self.is_sheep = False
            self.state = PlayerState.IDLE

        if self.is_holding:
            self.held_object.move_with_player(self.rect.x, self.rect.y - self.held_object.rect.height)
        
        if self.health <= 0:
            self.state = PlayerState.DEAD
        
        #Update animations
        match self.state:
            case PlayerState.SHEEP_IDLE:
                self.sheep_idle.update(delta_time)

            case PlayerState.SHEEP_WALKING:
                self.sheep_walk.update(delta_time)

            case PlayerState.SHEEP_BLEET:
                self.sheep_bleet.update(delta_time)
                
                if self.sheep_bleet.done:
                    self.state = PlayerState.SHEEP_IDLE
                    self.sheep_bleet.reset()

            case PlayerState.IDLE:
                self.idle.update(delta_time)

            case PlayerState.JUMPING:
                self.jump.update(delta_time)

            case PlayerState.WALKING:
                self.walk.update(delta_time)

            case PlayerState.ATTACKING:
                self.attack.update(delta_time)
                if self.attack.done:
                    self.state = PlayerState.IDLE
                    self.attack.reset()

            case PlayerState.DEAD:
                self.dead.update(delta_time)
                if self.dead.cur == self.dead.last:
                    self.rect.y += 10
            
            case PlayerState.SPECIAL_ATTACK:
                self.special_attack.update(delta_time)
                if self.special_attack.done:
                    self.state = PlayerState.IDLE
                    self.special_attack.reset()
            
    def handle_tile_collision(self, level, axis):
        min_col = int(self.bounding_box.x / TILE_SIZE)
        max_col = int((self.bounding_box.x + self.bounding_box.width) / TILE_SIZE)
        min_row = int(self.bounding_box.y / TILE_SIZE)
        max_row = int((self.bounding_box.y + self.bounding_box.height) / TILE_SIZE)

        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                
                if row < 0 or row >= TILE_ROWS or col < 0 or col >= TILE_COLS:
                    continue
                
                if level[row][col] == Tiles.SOLID:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    
                    if check_collision_recs(self.bounding_box, tile_rect):
                        
                        if axis == 'X':
                            if self.vx > 0: 
                                self.rect.x = tile_rect[0] - self.rect.width + 20
                                self.bounding_box.x = tile_rect[0] - self.bounding_box.width
                            elif self.vx < 0: 
                                self.rect.x = tile_rect[0] + TILE_SIZE - 20
                                self.bounding_box.x = tile_rect[0] + TILE_SIZE
                            self.vx = 0.0 
                            
                        elif axis == 'Y':
                            if self.vy >= 0: # Hitting Ground
                                self.rect.y = tile_rect[1] - self.rect.height
                                self.bounding_box.y = tile_rect[1] - self.bounding_box.height
                                self.is_grounded = True
                                if self.state == PlayerState.JUMPING:
                                    self.state = PlayerState.IDLE
                                    self.jump.reset()

                            elif self.vy < 0: # Hitting Ceilling
                                self.rect.y = tile_rect[1] + TILE_SIZE
                                self.bounding_box.y = tile_rect[1] + TILE_SIZE
                                
                            self.vy = 0.0 
                            
    
    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False

    def hold_object(self, held_object):
        if self.is_holding:
            held_object.is_held = True
            self.held_object = held_object

    def draw(self):
        match self.state:
            case PlayerState.SHEEP_IDLE:
                frame = self.sheep_idle.frame(self.width, 8)
                frame.width *= self.player_direction
                draw_texture_pro(self.sheep_texture, frame, self.rect, Vector2(0, 0), 0.0, WHITE)

            case PlayerState.SHEEP_WALKING:
                frame = self.sheep_walk.frame(self.width, 8)
                frame.width *= self.player_direction
                draw_texture_pro(self.sheep_texture, frame, self.rect, Vector2(0, 0), 0.0, WHITE)
                
            case PlayerState.SHEEP_BLEET:
                frame = self.sheep_bleet.frame(self.width, 8)
                frame.width *= self.player_direction
                draw_texture_pro(self.sheep_texture, frame, self.rect, Vector2(0, 0), 0.0, WHITE)

            case PlayerState.ATTACKING:
                frame = self.attack.frame(self.width, 8)
                frame.width *= self.player_direction
                draw_texture_pro(self.texture, frame, self.rect, Vector2(0, 0), 0.0, WHITE)

            case PlayerState.IDLE:
                frame = self.idle.frame(self.width, 2)
                frame.width *= self.player_direction
                draw_texture_pro(self.texture, frame, self.rect, Vector2(0, 0), 0.0, WHITE)

            case PlayerState.JUMPING:
                frame = self.jump.frame(self.width, 3)
                frame.width *= self.player_direction
                draw_texture_pro(self.texture, frame, self.rect, Vector2(0, 0), 0.0, WHITE)

            case PlayerState.WALKING:
                frame = self.walk.frame(self.width, 11)
                frame.width *= self.player_direction
                draw_texture_pro(self.texture, frame, self.rect, Vector2(0, 0), 0.0, WHITE)

            case PlayerState.DEAD:
                draw_texture_pro(self.texture, self.dead.frame(self.width, 20), self.rect, Vector2(0, 0), 0.0, WHITE)

            case PlayerState.SPECIAL_ATTACK:
                frame = self.special_attack.frame(self.width, 5)
                frame.width *= self.player_direction
                draw_texture_pro(self.texture, frame, self.rect, Vector2(0, 0), 0.0, WHITE)
        
        self.health_bar.draw()
    
    def shutdown(self):
        unload_texture(self.texture)

