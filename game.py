from pyray import *
from utils.level import Level
from components.player import Player
from settings import *
from enums import PlayerState, CyclopsState, GameState
from components.cyclops import Cyclops
from screens.level_one import Level_One

from screens.startup_screen import Startup_Screen
from screens.instructions import Instruction_Screen
from screens.pause import Pause_Screen
from screens.game_over import Game_Over
from screens.level_two import Level_Two

class Game:
    def __init__(self):
        self.player = Player(TILE_SIZE * 2, TILE_SIZE * 2) 
        self.level_one = Level_One(self.player)
        self.start_up = Startup_Screen()
        self.instructions = Instruction_Screen()
        self.pause = Pause_Screen()
        self.game_over = Game_Over()
        self.level_two = Level_Two(self.player)

        self.game_state = GameState.LEVEL_TWO
        
        self.held_sheep_index = None

    def startup(self):
        self.player.startup()
        self.start_up.startup()
        self.level_one.startup()
        self.instructions.startup()
        self.pause.startup()
        self.game_over.startup()
        self.level_two.startup()

    def update(self):
        delta_time = get_frame_time()

        match self.game_state:
            case GameState.STARTUP:
                self.start_up.update(delta_time)
                if is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.game_state = GameState.INSTRUCTIONS
            case GameState.INSTRUCTIONS:
                if is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.game_state = GameState.LEVEL_ONE
            case GameState.LEVEL_ONE:
                self.level_one.update(self.player, delta_time)
                if is_key_pressed(KeyboardKey.KEY_P):
                    self.game_state = GameState.PAUSE
                if self.player.health < 0 and self.player.dead.done:
                    self.game_state = GameState.GAME_OVER
            case GameState.PAUSE:
                if is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.game_state = GameState.LEVEL_ONE
                if is_key_pressed(KeyboardKey.KEY_I):
                    self.game_state = GameState.INSTRUCTIONS
            case GameState.GAME_OVER:
                if is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.level_one.shutdown()
                    self.player.shutdown()
                    self.level_one.__init__()
                    self.level_one.startup()
                    self.player.__init__(TILE_SIZE * 2, TILE_SIZE * 2)
                    self.player.startup()
                    self.game_state = GameState.LEVEL_ONE  
                    print(self.game_state)
            case GameState.LEVEL_TWO:
                self.level_two.update(self.player, delta_time)
                if is_key_pressed(KeyboardKey.KEY_P):
                    self.game_state = GameState.PAUSE
                if self.player.health < 0 and self.player.dead.done:
                    self.game_state = GameState.GAME_OVER


    def draw(self):
        match self.game_state:
            case GameState.STARTUP:
                self.start_up.draw()
            case GameState.INSTRUCTIONS:
                self.instructions.draw()
            case GameState.LEVEL_ONE:
                self.level_one.draw(self.player) 
            case GameState.PAUSE:
                self.pause.draw()
            case GameState.GAME_OVER:
                self.game_over.draw()
            case GameState.LEVEL_TWO:
                self.level_two.draw(self.player)
                  

    def shutdown(self):
        self.player.shutdown()
        self.level_one.shutdown()
        self.start_up.shutdown()
        self.instructions.shutdown()
        self.pause.shutdown()
        self.game_over.shutdown()
        self.level_two.shutdown()

