from pyray import *
from utils.level import Level
from settings import *
from enums import PlayerState, CyclopsState, GameState
from utils.camera import Camera

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
        self.island_background = load_texture(str(THIS_DIR) + "\\resources\\background.png")
        self.island_background_rec = (0, 0, self.island_background.width, self.island_background.height)

    def update(self, player, delta_time):

        player.update(delta_time, self.game_level)
        self.cyclopses.update(self.game_level, player, delta_time)
        self.sheeps.update(self.game_level, delta_time)
        self.camera.update(player, GameState.LEVEL_ONE)

        if not player.is_sheep:
            self.handle_hay_collection(player)
            self.handle_sheep_interaction(player)
            self.handle_cyclops_interaction(player, delta_time)

        self.handle_vase_interaction(player)

        if self.door.locked and self.sheeps.sheep_collected():
            self.door.locked = False
        
        if not self.door.locked and player.is_sheep:
            if check_collision_recs(player.rect, self.door.rect_door) and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                self.door.open = True

    def draw(self, player):
        draw_texture_pro(self.island_background, self.island_background_rec, self.rec, Vector2(0,0), 0, WHITE)
        self.hay.draw_hay_count(player.hay)
             
        begin_mode_2d(self.camera.camera)
        
        self.door.draw()
        self.fences.draw()
        self.blocks.draw()
        self.hay.draw()       
        self.vases.draw() 
        self.cyclopses.draw()
        self.sheeps.draw()
        player.draw()
        
        end_mode_2d()
    
    def shutdown(self):
        self.door.shutdown()
        self.fences.shutdown()        
        self.vases.shutdown()
        self.blocks.shutdown()
        self.sheeps.shutdown()
        self.hay.shutdown()
        self.cyclopses.shutdown()
    
    def check_collection(self, player):
        collected_indices = []
        
        for i, hay in enumerate(self.hay.collection):
            
            if check_collision_recs(player.rect, hay) and is_key_pressed(KeyboardKey.KEY_F):
                collected_indices.append(i)
                
        return collected_indices
    
    def check_collision(self, player, entities):
        
        for i, entity in enumerate(entities):

            if check_collision_recs(player.bounding_box, entity.rect):
                return i
                              
        return -1

    def handle_hay_collection(self, player):
        collected_indices = self.check_collection(player)
        if collected_indices:
            for index in sorted(collected_indices, reverse=True):
                self.hay.collection.pop(index)
                player.hay += 1

    def handle_vase_interaction(self, player):
        collided_vase = self.check_collision(player, self.vases.collection)
        if collided_vase >= 0 and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT) and self.vases.collection[collided_vase].full:
            if not player.is_sheep:
                self.vases.collection[collided_vase].full = False
                player.hay += 3
            else:
                player.state = PlayerState.SHEEP_BLEET
    
    def handle_sheep_interaction(self, player):
        collided_sheep = self.check_collision(player, self.sheeps.collection)
        if collided_sheep >= 0 and is_key_pressed(KeyboardKey.KEY_F):
            if player.hay > 0:
                self.sheeps.collection[collided_sheep].hay += 1
                player.hay -= 1
                player.can_transform = True
        if collided_sheep >= 0 and is_key_pressed(KeyboardKey.KEY_R) and self.sheeps.collection[collided_sheep].is_friendly:
            player.is_holding = True
            self.held_sheep_index = collided_sheep
            player.hold_object(self.sheeps.collection[collided_sheep])

        if is_key_pressed(KeyboardKey.KEY_G) and player.is_holding == True:
            self.sheeps.collection[self.held_sheep_index].is_grounded = False
            
            self.sheeps.collection[self.held_sheep_index].is_held = False
            player.is_holding = False
    
    def handle_cyclops_interaction(self, player, delta_time):
        collided_enemy = self.check_collision(player, self.cyclopses.collection)
        if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
                player.state = PlayerState.ATTACKING
        if collided_enemy != -1 and self.cyclopses.collection[collided_enemy].state != CyclopsState.DEAD:
            if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
                    self.cyclopses.collection[collided_enemy].health -= 25
            player.health -= self.cyclopses.collection[collided_enemy].attack(delta_time)


