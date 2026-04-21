class PlayerState(enumerate):
    WALKING = 0
    HOLDING_SHEEP = 1
    HOLDING_CREW = 2
    ATTACKING = 3
    SNEAK = 4
    SHEEP = 5
    POWER_ATTACK = 6 
    IDLE = 7
    JUMPING = 8
    SHEEP_IDLE = 9
    SHEEP_WALKING = 10
    SHEEP_SNEAK = 11
    SHEEP_ATTACKING = 12
class Tiles(enumerate):
    AIR = 0
    SOLID = 1
    SHEEP = 2 
    ENEMY = 3
    HAY = 4 
    BOUNDARY = 5
    VASE_EMPTY = 6
    VASE_FULL = 7
    

class Axis(enumerate):
    X_AXIS = 0
    Y_AXIS = 1