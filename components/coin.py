from pyray import *
from settings import *

class Coin:
    def draw(coins):
        radius = TILE_SIZE * 0.3 / 2 
    
        for cx, cy in coins:
            v1 = Vector2(cx, cy - radius * 2)
            v2 = Vector2(cx + radius * 1.5, cy)
            v3 = Vector2(cx, cy + radius * 2)
            v4 = Vector2(cx - radius * 1.5, cy)
            
            draw_triangle(v1, v2, v4, YELLOW)
            draw_triangle(v2, v3, v4, GOLD)
            
            draw_line_v(v1, v3, BLACK)
            draw_line_v(v2, v4, BLACK)