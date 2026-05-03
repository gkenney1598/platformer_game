from pyray import *
from settings import *
from utils.level import Level
from enums import PlayerState, CyclopsState, GameState
from utils.camera import Camera

class Level_Two:
    def __init__(self, player):
        self.level, self.solid, self.cyclopses, self.vases, self.gold, self.altar, self.athena, self.crewmates = Level.parse_level_two(LEVEL_TWO)

        self.cave_texture = None

        self.camera = Camera(Vector2(player.rect.x, player.rect.y), Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 2.5)
        self.mini_map = Camera(Vector2(player.rect.x, player.rect.y), Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), .25)

        self.screen_mini_map = None 
        self.mini_map_rect = Rectangle(0, SCREEN_HEIGHT, int(SCREEN_WIDTH / 4),  int(-SCREEN_HEIGHT / 4))
        self.mini_map_dest = Rectangle(int(SCREEN_WIDTH / 4 * 3 - 50), 50, int(SCREEN_WIDTH / 4), int(SCREEN_HEIGHT / 4))

        self.screen_camera = None
        self.camera_rect = Rectangle(0, 0, SCREEN_WIDTH, -SCREEN_HEIGHT)

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\.\\resources\\cave.png")
        self.screen_camera = load_render_texture(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))
        self.screen_mini_map = load_render_texture(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))

        self.solid.startup(self.texture)
        self.altar.startup(self.texture)
        self.cyclopses.startup()
        self.vases.startup()
        self.gold.startup()
        self.athena.startup()
        self.crewmates.startup()
        
    
    def update(self, player, delta_time):
        player.update(delta_time, self.level)
        self.cyclopses.update(self.level, player, delta_time)

        self.camera.update(player, GameState.LEVEL_TWO)
        self.mini_map.update(player, GameState.LEVEL_TWO, True)


        self.crewmates.update(self.level, delta_time)

        self.handle_vase_interaction(player)
        self.handle_altar_interaction(player)
        self.handle_crewmate_interaction(player)

        if not player.is_sheep:
            self.handle_gold_collection(player)
            self.handle_cyclops_interaction(player, delta_time)

        if self.athena.shown:
            self.athena.update(delta_time)
    
    def draw(self, player):

        begin_texture_mode(self.screen_camera) 
        begin_mode_2d(self.camera.camera)
        clear_background(CAVE_BACKGROUND)

        self.draw_map(player, False)

        end_mode_2d()
        end_texture_mode()

        begin_texture_mode(self.screen_mini_map)
        begin_mode_2d(self.mini_map.camera)
        clear_background(CAVE_BACKGROUND)

        self.draw_map(player, True)

        end_mode_2d()
        end_texture_mode()

        
        draw_texture_rec(self.screen_camera.texture, self.camera_rect, Vector2(0,0), WHITE)   
        draw_texture_rec(self.screen_mini_map.texture, self.mini_map_rect, Vector2(int(SCREEN_WIDTH / 4 * 3 - 50), 50), WHITE)
        draw_rectangle_lines_ex(self.mini_map_dest, 5, WHITE)
        self.gold.draw_gold_count(player.gold)
        self.crewmates.draw_mate_count()


    def draw_map(self, player, is_mini):
        
        if not is_mini:
            self.cyclopses.draw()
            self.vases.draw()
            self.gold.draw()
            self.altar.draw()
            self.crewmates.draw()
        
        self.solid.draw()
        player.draw()

        if self.athena.shown:
            self.athena.draw()
            
    
    def shutdown(self):
        self.cyclopses.shutdown()
        self.vases.shutdown()
        self.gold.shutdown()
        self.athena.shutdown()
        self.crewmates.draw()

        unload_texture(self.texture)
        unload_render_texture(self.screen_camera)
        unload_render_texture(self.screen_mini_map)

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

        
