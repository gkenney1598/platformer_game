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
        self.is_holding = False
        self.state = PlayerState.IDLE
        self.held_object = None
        self.can_transform = False

        self.health = 100
        self.health_bar = HealthBar(self.health, (self.rect.x + self.rect.width) / 4, y, self.rect.width, 5)

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
        
    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\resources\odysseus.png")
        self.width = int(self.texture.width) / 13
        self.rect.width = self.width
        self.height = self.texture.height / 21
        self.rect.height = self.height
        self.bounding_box = Rectangle(self.rect.x + 10, self.rect.y, self.width - 40, self.height)

    def update(self, delta_time, level, held_object = None):
        self.vx = 0.0
        if is_key_down(KeyboardKey.KEY_LEFT) or is_key_down(KeyboardKey.KEY_A):
            self.vx = -PLAYER_SPEED
            self.player_direction = Direction.LEFT
            if self.state != PlayerState.JUMPING:
                self.state = PlayerState.WALKING
        if is_key_down(KeyboardKey.KEY_RIGHT) or is_key_down(KeyboardKey.KEY_D):
            self.vx = PLAYER_SPEED
            self.player_direction = Direction.RIGHT
            if self.state != PlayerState.JUMPING:
                self.state = PlayerState.WALKING
        if is_key_released(KeyboardKey.KEY_LEFT) or is_key_released(KeyboardKey.KEY_A) or is_key_released(KeyboardKey.KEY_RIGHT) or is_key_released(KeyboardKey.KEY_D):
            self.state = PlayerState.IDLE
        

        if self.is_grounded:
            self.vy = 0.0
            
        if (is_key_pressed(KeyboardKey.KEY_SPACE) or is_key_pressed(KeyboardKey.KEY_UP)) and self.is_grounded:
            self.vy = JUMP_VELOCITY
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
            self.state = PlayerState.SHEEP_IDLE
        if is_key_pressed(KeyboardKey.KEY_Y):
            self.state = PlayerState.IDLE

        if self.is_holding:
            self.held_object.move_with_player(self.rect.x, self.rect.y - self.held_object.rect.height)
        
        if self.health <= 0:
            self.state = PlayerState.DEAD
        
        match self.state:
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
        
    def handle_tile_collision(self, level, axis):
        """Performs AABB collision checks against solid tiles and resolves the collision."""
        player_rect = self.bounding_box
        px, py, pw, ph = player_rect.x, player_rect.y, player_rect.width, player_rect.height
        
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
                    
                    if check_collision_recs(player_rect, tile_rect):
                        
                        if axis == 'X':
                            if self.vx > 0: # Moving Right
                                self.rect.x = tile_rect[0] - self.rect.width + 20
                                self.bounding_box.x = tile_rect[0] - self.bounding_box.width
                            elif self.vx < 0: # Moving Left
                                self.rect.x = tile_rect[0] + TILE_SIZE - 20
                                self.bounding_box.x = tile_rect[0] + TILE_SIZE
                            self.vx = 0.0 
                            
                        elif axis == 'Y':
                            if self.vy >= 0: # Falling (Hitting Ground)
                                self.rect.y = tile_rect[1] - self.rect.height
                                self.bounding_box.y = tile_rect[1] - self.bounding_box.height
                                self.is_grounded = True
                                if self.state == PlayerState.JUMPING:
                                    self.state = PlayerState.IDLE
                                    self.jump.reset()
                                # print("grounded")
                            elif self.vy < 0: # Jumping (Hitting Ceiling)
                                self.rect.y = tile_rect[1] + TILE_SIZE
                                self.bounding_box.y = tile_rect[1] + TILE_SIZE
                                
                            self.vy = 0.0 
                            
                        player_rect = self.bounding_box
                        px, py, pw, ph = player_rect.x, player_rect.y, player_rect.width, player_rect.height

                elif level[row][col] == Tiles.HAY:
                    tile_rect = (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if check_collision_recs(player_rect, tile_rect):
                        level[row][col] == Tiles.AIR
                        self.hay += 1
                        
    def check_collection(self, hay):
        """Checks for collision with coins and returns indices of collected coins."""
        collected_indices = []
        player_rect = self.rect
        
        for i, hay in enumerate(hay):
            
            if check_collision_recs(player_rect, hay.rect) and is_key_pressed(KeyboardKey.KEY_F):
                collected_indices.append(i)
                
        return collected_indices
    
    def check_sheep_collision(self, sheep):
        
        for i, sheep in enumerate(sheep):

            if check_collision_recs(self.bounding_box, sheep.rect):
                return i
                              
        return -1
    
    def check_vase_collision(self, vase):
        for i, vase in enumerate(vase):
            if check_collision_recs(self.bounding_box, vase.rect):
                return i 
            
        return -1
    
    def check_enemy_collision(self, enemies):
        for i, enemy in enumerate(enemies):
            if check_collision_recs(self.bounding_box, enemy.rect):
                return i
            
        return -1
    
    # def check_enemy_collision(self, enemies):
    #     """Checks for collision with enemies and determines outcome (stomp or death).
    #     Returns (hit_type, enemy_index) or (None, -1).
    #     hit_type: "STOMP" (safe kill) or "LETHAL" (death)
    #     """
    #     player_rect = self.get_rect()
    #     px, py, pw, ph = player_rect
        
    #     for i, enemy in enumerate(enemies):
    #         enemy_rect = enemy.get_rect()
            
    #         if check_collision_recs(player_rect, enemy_rect):
                
    #             # STOMP Condition: 
    #             # 1. Player is falling (vy > 0) 
    #             # 2. Player's bottom is above the enemy's mid-point (approximate stomping zone)
    #             is_stompable_zone = py + ph < enemy.y + enemy.height * 0.5 
                
    #             if self.vy > 0 and is_stompable_zone:
    #                 return "STOMP", i
    #             else:
    #                 # Lethal collision (side, head, or missing the stomp zone)
    #                 return "LETHAL", i
                    
    #     return None, -1
    
    def reset(self):
        """Resets the player to their starting position."""
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False

    def hold_object(self, held_object):
        if self.is_holding:
            held_object.is_held = True
            self.held_object = held_object
                
                # held_object.rect.x = self.rect.x
                # held_object.rect.y = self.rect.y - held_object.rect.height

    def draw(self):
        """Draws the player at their world coordinates."""
        match self.state:
            case PlayerState.SHEEP_IDLE:
                draw_rectangle_rec(self.rect, WHITE) 
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
        
        self.health_bar.draw()
    
    def shutdown(self):
        unload_texture(self.texture)

