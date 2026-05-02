from pyray import *
from settings import *
from utils.level import Level
from enums import PlayerState, CyclopsState

class Level_Two:
    def __init__(self):
        self.level, self.solid, self.cyclopses, self.vases, self.gold, self.altar, self.athena = Level.parse_level_two(LEVEL_TWO)

        self.cave_texture = None

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\.\\resources\\cave.png")
        self.solid.startup(self.texture)
        self.altar.startup(self.texture)
        self.cyclopses.startup()
        self.vases.startup()
        self.gold.startup()
        self.athena.startup()
        
    
    def update(self, player, delta_time, camera):
        player.update(delta_time, self.level)
        self.cyclopses.update(self.level, player, delta_time)
        camera.update(player)

        self.handle_vase_interaction(player)
        self.handle_altar_interaction(player)

        if not player.is_sheep:
            self.handle_gold_collection(player)
            self.handle_cyclops_interaction(player, delta_time)

        if self.athena.shown:
            self.athena.update(delta_time)
    
    def draw(self, player, camera):
        self.gold.draw_gold_count(player.gold)

        begin_mode_2d(camera.camera)

        
        self.solid.draw()
        self.cyclopses.draw()
        self.vases.draw()
        self.gold.draw()
        self.altar.draw()

        player.draw()

        if self.athena.shown:
            self.athena.draw()

        end_mode_2d()
    
    def shutdown(self):
        self.cyclopses.shutdown()
        self.vases.shutdown()
        self.gold.shutdown()
        self.athena.shutdown()

        unload_texture(self.texture)

    def check_collection(self, player):
        collected_indices = []
        
        for i, gold in enumerate(self.gold.collection):
            
            if check_collision_recs(player.rect, gold) and is_key_pressed(KeyboardKey.KEY_F):
                collected_indices.append(i)
                
        return collected_indices
    
    def check_collision(self, player, entities):
        
        for i, entity in enumerate(entities):

            if check_collision_recs(player.bounding_box, entity.rect):
                return i
                              
        return -1

    def handle_gold_collection(self, player):
        collected_indices = self.check_collection(player)
        if collected_indices:
            for index in sorted(collected_indices, reverse=True):
                self.gold.collection.pop(index)
                player.gold += 1

    def handle_vase_interaction(self, player):
        collided_vase = self.check_collision(player, self.vases.collection)
        if collided_vase >= 0 and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT) and self.vases.collection[collided_vase].full:
            if not player.is_sheep:
                self.vases.collection[collided_vase].full = False
                player.gold += 3
            else:
                player.state = PlayerState.SHEEP_BLEET
    
    def handle_altar_interaction(self, player):
        if check_collision_recs(player.bounding_box, self.altar.rect_pillar) and is_key_pressed(KeyboardKey.KEY_F):
            self.altar.gold += player.gold
            player.gold = 0
            if self.altar.gold == TOTAL_GOLD:
                self.altar.offer_complete = True
                self.athena.shown = True


    # something similar will be needed for crewmates
    # def handle_sheep_interaction(self, player):
    #     collided_sheep = self.check_collision(player, self.sheeps.collection)
    #     if collided_sheep >= 0 and is_key_pressed(KeyboardKey.KEY_F):
    #         if player.hay > 0:
    #             self.sheeps.collection[collided_sheep].hay += 1
    #             player.hay -= 1
    #             player.can_transform = True
    #     if collided_sheep >= 0 and is_key_pressed(KeyboardKey.KEY_R) and self.sheeps.collection[collided_sheep].is_friendly:
    #         player.is_holding = True
    #         self.held_sheep_index = collided_sheep
    #         player.hold_object(self.sheeps.collection[collided_sheep])

    #     if is_key_pressed(KeyboardKey.KEY_G) and player.is_holding == True:
    #         self.sheeps.collection[self.held_sheep_index].is_grounded = False
            
    #         self.sheeps.collection[self.held_sheep_index].is_held = False
    #         player.is_holding = False
    
    def handle_cyclops_interaction(self, player, delta_time):
        collided_enemy = self.check_collision(player, self.cyclopses.collection)
        if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
                player.state = PlayerState.ATTACKING
        if collided_enemy != -1 and self.cyclopses.collection[collided_enemy].state != CyclopsState.DEAD:
            if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
                    self.cyclopses.collection[collided_enemy].health -= 25
            player.health -= self.cyclopses.collection[collided_enemy].attack(delta_time)
