from pyray import *
from utils.level import Level
from components.player import Player
from settings import *
from enums import PlayerState, CyclopsState, GameState
from components.cyclops import Cyclops
from levels.level_one import Level_One
from utils.camera import Camera

class Game:
    def __init__(self):
        self.level_one = Level_One()
        self.player = Player(TILE_SIZE * 2, TILE_SIZE * 2) 
        self.game_state = GameState.LEVEL_ONE
        
        # --- Camera Initialization ---
        self.camera = Camera(self.player.rect)


        self.held_sheep_index = None

    def startup(self):
        self.player.startup()

        match self.game_state:
            case GameState.LEVEL_ONE:
                self.level_one.startup()

    def update(self):
        delta_time = get_frame_time()
    
        match self.game_state:
            case GameState.LEVEL_ONE:
                self.level_one.update(self.player, delta_time, self.camera)

    def draw(self):
        match self.game_state:
            case GameState.LEVEL_ONE:
                self.level_one.draw(self.player, self.camera)         

    def shutdown(self):
        self.player.shutdown()
        self.level_one.shutdown()

