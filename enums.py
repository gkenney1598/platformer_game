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
class Tiles(enumerate):
    AIR = 0
    SOLID = 1
    SHEEP = 2 
    ENEMY = 3
    HAY = 4 

class Axis(enumerate):
    X_AXIS = 0
    Y_AXIS = 1