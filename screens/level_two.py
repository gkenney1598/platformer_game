from pyray import *
from settings import *
from utils.level import Level
from enums import GameState
from utils.camera import Camera
from utils.interaction import Interaction
from utils.collision import Collision

class Level_Two:
    def __init__(self, player):
        self.level, self.solid, self.cyclopses, self.vases, self.gold, self.altar, self.athena, self.crewmates = Level.parse_level_two(LEVEL_TWO)
        self.player = player

        self.cave_texture = None

        self.camera = Camera(Vector2(player.rect.x, player.rect.y), Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 2.5)
        self.mini_map = Camera(Vector2(player.rect.x, player.rect.y), Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), .25)

        self.screen_mini_map = None 
        self.mini_map_rect = Rectangle(0, SCREEN_HEIGHT, int(SCREEN_WIDTH / 4),  int(-SCREEN_HEIGHT / 4))
        self.mini_map_dest = Rectangle(int(SCREEN_WIDTH / 4 * 3 - 50), 50, int(SCREEN_WIDTH / 4), int(SCREEN_HEIGHT / 4))

        self.screen_camera = None
        self.camera_rect = Rectangle(0, 0, SCREEN_WIDTH, -SCREEN_HEIGHT)

    def startup(self):
        self.texture = load_texture(str(THIS_DIR) + "\\.\\resources\\level_two\\cave.png")
        self.screen_camera = load_render_texture(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))
        self.screen_mini_map = load_render_texture(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))

        self.solid.startup(self.texture)
        self.altar.startup(self.texture)
        self.cyclopses.startup()
        self.vases.startup()
        self.gold.startup()
        self.athena.startup()
        self.crewmates.startup()
        
    
    def update(self, delta_time):
        self.player.update(delta_time, self.level)
        self.cyclopses.update(self.level, self.player, delta_time)

        self.camera.update(self.player, GameState.LEVEL_TWO)
        self.mini_map.update(self.player, GameState.LEVEL_TWO, True)


        self.crewmates.update(self.level, delta_time)

        self.player.gold += Interaction.handle_vase_interaction(self.player, self.vases)
        self.handle_altar_interaction(self.player)
        self.handle_crewmate_interaction(self.player)

        if not self.player.is_sheep:
            self.player.gold += Interaction.handle_collection(self.player, self.gold)
            Interaction.handle_cyclops_interaction(self.player, delta_time, self.cyclopses)

        if self.athena.shown:
            self.athena.update(delta_time)
    
    def draw(self):

        begin_texture_mode(self.screen_camera) 
        begin_mode_2d(self.camera.camera)
        clear_background(CAVE_BACKGROUND)

        self.draw_map(False)

        end_mode_2d()
        end_texture_mode()

        begin_texture_mode(self.screen_mini_map)
        begin_mode_2d(self.mini_map.camera)
        clear_background(CAVE_BACKGROUND)

        self.draw_map(True)

        end_mode_2d()
        end_texture_mode()

        
        draw_texture_rec(self.screen_camera.texture, self.camera_rect, Vector2(0,0), WHITE)   
        draw_texture_rec(self.screen_mini_map.texture, self.mini_map_rect, Vector2(int(SCREEN_WIDTH / 4 * 3 - 50), 50), WHITE)
        draw_rectangle_lines_ex(self.mini_map_dest, 5, WHITE)
        self.gold.draw_gold_count(self.player.gold)
        self.crewmates.draw_mate_count()


    def draw_map(self, is_mini):
        
        if not is_mini:
            self.cyclopses.draw()
            self.vases.draw()
            self.gold.draw()
            self.altar.draw()
            self.crewmates.draw()
        
        self.solid.draw()
        self.player.draw()

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
    
    def handle_altar_interaction(self, player):
        if check_collision_recs(self.player.bounding_box, self.altar.rect_pillar) and is_key_pressed(KeyboardKey.KEY_F):
            self.altar.gold += self.player.gold
            self.player.gold = 0
            if self.altar.gold == TOTAL_GOLD:
                self.altar.offer_complete = True
                self.athena.shown = True
                self.player.can_special_attack = True

    def handle_crewmate_interaction(self, player):
        collided_mate = Collision.check_collision(player, self.crewmates.collection)
        if collided_mate >= 0 and is_key_pressed(KeyboardKey.KEY_R):
            self.crewmates.collection[collided_mate].is_collected = True
            self.crewmates.total_collected += 1

        
