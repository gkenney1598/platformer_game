from pyray import *
from components.level import Level
from components.player import Player
from settings import *
from enums import PlayerState, CyclopsState
from components.cyclops import Cyclops

class Game:
    def __init__(self):
        self.game_level, self.sheeps, self.cyclopses, self.hay, self.vases, self.blocks = Level.parse_level(LEVEL)
        self.player = Player(TILE_SIZE * 2, TILE_SIZE * 2) 
        self.score = 0
        self.game_state = "PLAYING" 
        
        # --- Camera Initialization ---
        self.camera = Camera2D()
        self.camera.target = Vector2(self.player.rect.x, self.player.rect.y) 
        self.camera.offset = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) 
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0


        self.held_sheep_index = None
        self.background = None
        self.background_rec = None
        self.rec = Rectangle(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)

    def startup(self):
        self.player.startup()
        self.vases.startup()
        self.blocks.startup()
        self.sheeps.startup()
        self.hay.startup()
        self.cyclopses.startup()
        self.background = load_texture(str(THIS_DIR) + "\\resources\\background.png")
        self.background_rec = (0, 0, self.background.width, self.background.height)

    def update(self):
        delta_time = get_frame_time()
        
        # --- Update ---
        if self.game_state == "PLAYING":
            self.player.update(delta_time, self.game_level)
            
            # Update Enemies
            for cyclops in self.cyclopses.collection:
                cyclops.update(delta_time, self.game_level, self.player.rect)
                if not self.player.is_sheep:
                    cyclops.check_player_nearby(self.player.attention_box)

            for sheep in self.sheeps.collection:
                sheep.update(delta_time, self.game_level)

            self.camera_update(self.camera, self.player, WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

            if not self.player.is_sheep:
                collected_indices = self.player.check_collection(self.hay.collection)
                if collected_indices:
                    for index in sorted(collected_indices, reverse=True):
                        self.hay.collection.pop(index)
                        self.player.hay += 1
                
                collided_sheep = self.player.check_sheep_collision(self.sheeps.collection)
                if collided_sheep >= 0 and is_key_pressed(KeyboardKey.KEY_F):
                    if self.player.hay > 0:
                        self.sheeps.collection[collided_sheep].hay += 1
                        self.player.hay -= 1
                        self.player.can_transform = True
                if collided_sheep >= 0 and is_key_pressed(KeyboardKey.KEY_R) and self.sheeps.collection[collided_sheep].is_friendly:
                    self.player.is_holding = True
                    self.held_sheep_index = collided_sheep
                    self.player.hold_object(self.sheeps.collection[collided_sheep])

            
                if is_key_pressed(KeyboardKey.KEY_G) and self.player.is_holding == True:
                    self.sheeps.collection[self.held_sheep_index].is_grounded = False
                    
                    self.sheeps.collection[self.held_sheep_index].is_held = False
                    self.player.is_holding = False
                    # self.player.state = PlayerState.IDLE

                collided_enemy = self.player.check_enemy_collision(self.cyclopses.collection)
                if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
                        self.player.state = PlayerState.ATTACKING
                if collided_enemy != -1 and self.cyclopses.collection[collided_enemy].state != CyclopsState.DEAD:
                    if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
                            self.cyclopses.collection[collided_enemy].health -= 25
                    self.player.health -= self.cyclopses.collection[collided_enemy].attack(delta_time)
            
            collided_vase = self.player.check_vase_collision(self.vases.collection)
            if collided_vase >= 0 and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT) and self.vases.collection[collided_vase].full:
                if not self.player.is_sheep:
                    self.vases.collection[collided_vase].full = False
                    self.player.hay += 3
                else:
                    self.player.state = PlayerState.SHEEP_BLEET

    def draw(self):
        draw_texture_pro(self.background, self.background_rec, self.rec, Vector2(0,0), 0, WHITE)
        begin_mode_2d(self.camera)
        
        self.blocks.draw()
        self.hay.draw(self.player.hay)       
        self.vases.draw() 
        self.cyclopses.draw()
        self.sheeps.draw()
        self.player.draw()
        
        end_mode_2d()

        # hay_text = f"Number of hay: {self.player.hay}"
        # draw_text(hay_text, 10, 40, 20, BLACK)

        

    def shutdown(self):
        self.player.shutdown()
        self.vases.shutdown()
        self.blocks.shutdown()
        self.sheeps.shutdown()
        self.hay.shutdown()
        self.cyclopses.shutdown()

    def camera_update(self, camera, player, world_width, world_height, screen_width, screen_height):
        """Centers the camera on the player and clamps the camera's target to the world bounds."""
        
        camera.target.x = player.rect.x + player.rect.width / 2
        camera.target.y = player.rect.y + player.rect.height / 2

        min_x = screen_width / 2
        max_x = world_width - screen_width / 2
        
        if camera.target.x < min_x:
            camera.target.x = min_x
        if camera.target.x > max_x:
            camera.target.x = max_x

        min_y = screen_height / 2
        max_y = world_height - screen_height / 2
        
        if camera.target.y < min_y:
            camera.target.y = min_y
        if camera.target.y > max_y:
            camera.target.y = max_y
        
        camera.offset.x = screen_width / 2
        camera.offset.y = screen_height / 2