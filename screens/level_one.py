from pyray import *
from utils.level import Level
from settings import *
from enums import PlayerState, CyclopsState, GameState
from utils.camera import Camera
from utils.collision import Collision
from utils.interaction import Interaction

class Level_One:
    def __init__(self, player):
        self.game_level, self.sheeps, self.cyclopses, self.hay, self.vases, self.blocks, self.fences, self.door = Level.parse_level_one(LEVEL_ONE)
        self.island_background = None
        self.island_background_rec = None
        self.rec = Rectangle(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        self.player = player
        self.camera = Camera(Vector2(player.rect.x, player.rect.y), Vector2(SCREEN_WIDTH / 2 + TILE_SIZE, SCREEN_HEIGHT / 2 - 35), 1.1)

    def startup(self):
        self.fences.startup()
        self.door.startup()
        self.vases.startup()
        self.blocks.startup()
        self.sheeps.startup()
        self.hay.startup()
        self.cyclopses.startup()
        self.island_background = load_texture(str(THIS_DIR) + "\\resources\\level_one\\background.png")
        self.island_background_rec = (0, 0, self.island_background.width, self.island_background.height)

    def update(self, delta_time):

        self.player.update(delta_time, self.game_level)
        self.cyclopses.update(self.game_level, self.player, delta_time)
        self.sheeps.update(self.game_level, delta_time)
        self.camera.update(self.player, GameState.LEVEL_ONE)

        if not self.player.is_sheep:
            self.player.hay += Interaction.handle_collection(self.player, self.hay)
            self.handle_sheep_interaction()
            Interaction.handle_cyclops_interaction(self.player, delta_time, self.cyclopses)

        self.player.hay += Interaction.handle_vase_interaction(self.player, self.vases)

        if self.door.locked and self.sheeps.sheep_collected():
            self.door.locked = False
        
        if not self.door.locked and self.player.is_sheep:
            if check_collision_recs(self.player.rect, self.door.rect_door) and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                self.door.open = True

    def draw(self):
        draw_texture_pro(self.island_background, self.island_background_rec, self.rec, Vector2(0,0), 0, WHITE)
        self.hay.draw_hay_count(self.player.hay)
             
        begin_mode_2d(self.camera.camera)
        
        self.door.draw()
        self.fences.draw()
        self.blocks.draw()
        self.hay.draw()       
        self.vases.draw() 
        self.cyclopses.draw()
        self.sheeps.draw()
        self.player.draw()
        
        end_mode_2d()
    
    def shutdown(self):
        self.door.shutdown()
        self.fences.shutdown()        
        self.vases.shutdown()
        self.blocks.shutdown()
        self.sheeps.shutdown()
        self.hay.shutdown()
        self.cyclopses.shutdown()
    
    def handle_sheep_interaction(self):
        collided_sheep = Collision.check_collision(self.player, self.sheeps.collection)
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


