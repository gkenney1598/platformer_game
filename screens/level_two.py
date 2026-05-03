from pyray import *
from settings import *
from utils.level import Level
from enums import PlayerState, CyclopsState

class Level_Two:
    def __init__(self):
        self.level, self.solid, self.cyclopses, self.vases, self.gold, self.altar, self.athena, self.crewmates = Level.parse_level_two(LEVEL_TWO)

        self.cave_texture = None

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\.\\resources\\cave.png")
        self.solid.startup(self.texture)
        self.altar.startup(self.texture)
        self.cyclopses.startup()
        self.vases.startup()
        self.gold.startup()
        self.athena.startup()
        self.crewmates.startup()
        
    
    def update(self, player, delta_time, camera):
        player.update(delta_time, self.level)
        self.cyclopses.update(self.level, player, delta_time)
        camera.update(player)
        self.crewmates.update(self.level, delta_time)

        self.handle_vase_interaction(player)
        self.handle_altar_interaction(player)
        self.handle_crewmate_interaction(player)

        if not player.is_sheep:
            self.handle_gold_collection(player)
            self.handle_cyclops_interaction(player, delta_time)

        if self.athena.shown:
            self.athena.update(delta_time)
    
    def draw(self, player, camera):
        self.gold.draw_gold_count(player.gold)
        self.crewmates.draw_mate_count()

        begin_mode_2d(camera.camera)

        
        self.solid.draw()
        self.cyclopses.draw()
        self.vases.draw()
        self.gold.draw()
        self.altar.draw()
        self.crewmates.draw()

        player.draw()

        if self.athena.shown:
            self.athena.draw()

        end_mode_2d()
    
    def shutdown(self):
        self.cyclopses.shutdown()
        self.vases.shutdown()
        self.gold.shutdown()
        self.athena.shutdown()
        self.crewmates.draw()

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
                player.can_special_attack = True

    def handle_crewmate_interaction(self, player):
        collided_mate = self.check_collision(player, self.crewmates.collection)
        if collided_mate >= 0 and is_key_pressed(KeyboardKey.KEY_R):
            self.crewmates.collection[collided_mate].is_collected = True
            self.crewmates.total_collected += 1
    
    def handle_cyclops_interaction(self, player, delta_time):
        collided_enemy = self.check_collision(player, self.cyclopses.collection)
        if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
            player.state = PlayerState.ATTACKING
        if is_key_pressed(KeyboardKey.KEY_Q) and player.can_special_attack:
            player.state = PlayerState.SPECIAL_ATTACK
        if collided_enemy != -1 and self.cyclopses.collection[collided_enemy].state != CyclopsState.DEAD:
            if self.cyclopses.collection[collided_enemy].boss:
                if is_key_released(KeyboardKey.KEY_Q):
                    self.cyclopses.collection[collided_enemy].health -= 10
            else: 
                if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
                        self.cyclopses.collection[collided_enemy].health -= 25
            player.health -= self.cyclopses.collection[collided_enemy].attack(delta_time)

        
