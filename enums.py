from enum import IntEnum
class PlayerState(enumerate):
    WALKING = 0
    ATTACKING = 1
    SHEEP = 2
    POWER_ATTACK = 3
    IDLE = 4
    JUMPING = 5
    SHEEP_IDLE =6
    SHEEP_WALKING = 7
    SHEEP_BLEET = 8
    DEAD = 9
class Tiles(enumerate):
    AIR = 0
    SOLID = 1
    SHEEP = 2 
    CYCLOPS = 3
    HAY = 4 
    BOUNDARY = 5
    VASE_EMPTY = 6
    VASE_FULL = 7
    
class SheepState(enumerate):
    IDLE = 0
    JUMP = 1

class Axis(enumerate):
    X_AXIS = 0
    Y_AXIS = 1

class CyclopsState(enumerate):
    WALKING = 0
    ANGRY = 1
    ATTACK = 2
    DEAD = 3

class AnimationType(IntEnum):
    REPEATING = 1
    ONESHOT = 2

class Direction(IntEnum):
    LEFT = -1
    RIGHT = 1

class GameState(enumerate):
    STARTUP = 0
    LEVEL_ONE = 1
    LEVEL_TWO = 2
    PAUSE = 3
    GAME_OVER = 4
    WIN = 5
