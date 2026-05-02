from pyray import *
from utils.level import Level
from components.player import Player
from settings import *
from enums import PlayerState, CyclopsState, GameState
from components.cyclops import Cyclops
from screens.level_one import Level_One
from utils.camera import Camera
from screens.startup_screen import Startup_Screen
from screens.instructions import Instruction_Screen
from screens.pause import Pause_Screen

class Game:
    def __init__(self):
        self.level_one = Level_One()
        self.start_up = Startup_Screen()
        self.instructions = Instruction_Screen()
        self.pause = Pause_Screen()
        self.player = Player(TILE_SIZE * 2, TILE_SIZE * 2) 
        self.game_state = GameState.STARTUP
        
        # --- Camera Initialization ---
        self.camera = Camera(self.player.rect)


        self.held_sheep_index = None

    def startup(self):
        self.player.startup()
        self.start_up.startup()
        self.level_one.startup()
        self.instructions.startup()
        self.pause.startup()

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
                self.level_one.update(self.player, delta_time, self.camera)
                if is_key_pressed(KeyboardKey.KEY_P):
                    self.game_state = GameState.PAUSE
            case GameState.PAUSE:
                if is_key_pressed(KeyboardKey.KEY_ENTER):
                    self.game_state = GameState.LEVEL_ONE
                if is_key_pressed(KeyboardKey.KEY_I):
                    self.game_state = GameState.INSTRUCTIONS              

    def draw(self):
        match self.game_state:
            case GameState.STARTUP:
                self.start_up.draw()
            case GameState.INSTRUCTIONS:
                self.instructions.draw()
            case GameState.LEVEL_ONE:
                self.level_one.draw(self.player, self.camera) 
            case GameState.PAUSE:
                self.pause.draw()
                  

    def shutdown(self):
        self.player.shutdown()
        self.level_one.shutdown()
        self.start_up.shutdown()
        self.instructions.shutdown()
        self.draw.shutdown()

