from pyray import *
from settings import *

from enum import IntEnum

class AnimationType(IntEnum):
    REPEATING = 1
    ONESHOT = 2

class Direction(IntEnum):
    LEFT = -1
    RIGHT = 1

class Animation:
    def __init__(self, first, last, cur, step, duration, duration_left, anim_type, row, sprites_in_row):
        self.first = first
        self.last = last
        self.cur = cur
        self.step = step
        self.duration = duration
        self.duration_left = duration_left
        self.type = anim_type
        self.row = row
        self.sprites_in_row = sprites_in_row 
        self.done = False

    def update(self, dt):
        self.duration_left -= dt
        
        if (self.duration_left<=0):
            self.duration_left = self.duration
            self.cur += self.step

            if (self.cur > self.last):
                match(self.type):
                    case AnimationType.ONESHOT:
                        self.cur = self.last 
                        self.done = True
                    case AnimationType.REPEATING:
                        self.cur = self.first 

    def frame(self, tile_size, row):
        x = (self.cur % self.sprites_in_row) * tile_size
        y =  tile_size * self.row

        return Rectangle(x, y, tile_size, tile_size)

    def reset(self): # ADDED
        self.cur = self.first
        self.done = False