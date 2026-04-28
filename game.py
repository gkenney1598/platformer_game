from pyray import *
from components.level import Level
from components.player import Player
from settings import *
from enums import PlayerState, CyclopsState
from components.cyclops import Cyclops

class Game:
    def __init__(self):
        self.game_level, self.sheep, self.cyclops, self.hay, self.vase, = Level.parse_level(LEVEL)
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

    def startup(self):
        self.player.startup()

    def update(self):
        delta_time = get_frame_time()
        
        # --- Update ---
        if self.game_state == "PLAYING":
            self.player.update(delta_time, self.game_level)
            
            # Update Enemies
            for cyclops in self.cyclops:
                cyclops.update(delta_time, self.game_level, self.player.rect)
                cyclops.check_player_nearby(self.player.attention_box)

            for sheep in self.sheep:
                sheep.update(delta_time, self.game_level)

            self.camera_update(self.camera, self.player, WORLD_WIDTH, WORLD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT)

            #TODO: all this collision stuff to seperate functions
            collected_indices = self.player.check_collection(self.hay)
            if collected_indices:
                for index in sorted(collected_indices, reverse=True):
                    self.hay.pop(index)
                    self.player.hay += 1
            
            collided_sheep = self.player.check_sheep_collision(self.sheep)
            if collided_sheep >= 0 and is_key_pressed(KeyboardKey.KEY_F):
                if self.player.hay > 0:
                    self.sheep[collided_sheep].hay += 1
                    self.player.hay -= 1
                    self.player.can_transform = True
            if collided_sheep >= 0 and is_key_pressed(KeyboardKey.KEY_R) and self.sheep[collided_sheep].is_friendly:
                self.player.is_holding = True
                self.held_sheep_index = collided_sheep
                self.player.hold_object(self.sheep[collided_sheep])

        
            if is_key_pressed(KeyboardKey.KEY_G) and self.player.is_holding == True:
                self.sheep[self.held_sheep_index].is_grounded = False
                
                self.sheep[self.held_sheep_index].is_held = False
                self.player.is_holding = False
                # self.player.state = PlayerState.IDLE

            collided_vase = self.player.check_vase_collision(self.vase)
            if collided_vase >= 0 and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT) and self.vase[collided_vase].full:
                self.vase[collided_vase].full = False
                self.player.hay += 3

            collided_enemy = self.player.check_enemy_collision(self.cyclops)
            if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
                    self.player.state = PlayerState.ATTACKING
            if collided_enemy != -1 and self.cyclops[collided_enemy].state != CyclopsState.DEAD:
                if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
                        self.cyclops[collided_enemy].health -= 25
                self.player.health -= self.cyclops[collided_enemy].attack(delta_time)
            # else:
            #     self.player.state = PlayerState.IDLE

    def draw(self):
        begin_mode_2d(self.camera)
        
        Level.draw_level(self.game_level)

        for hay in self.hay:
            hay.draw()
        
        for vase in self.vase:
            vase.draw()
            
        for cyclops in self.cyclops:
            cyclops.draw()

        for sheep in self.sheep:
            sheep.draw()

        self.player.draw()
        
        # End the 2D camera mode
        end_mode_2d()
        
        # 5. Draw HUD (Drawn on screen, outside of BeginMode2D)
        score_text = f"Score: {self.score}".encode('utf-8')
        draw_text(score_text, SCREEN_WIDTH - measure_text(score_text, 20) - 10, 10, 20, BLACK)
        
        debug_text = f"Grounded: {self.player.is_grounded}".encode('utf-8')
        draw_text(debug_text, 10, 10, 20, BLACK) 

        hay_text = f"Number of hay: {self.player.hay}"
        draw_text(hay_text, 10, 40, 20, BLACK)

    def shutdown(self):
        self.player.shutdown()

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