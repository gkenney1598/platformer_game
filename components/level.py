from pyray import *
from settings import *
from enums import Tiles
from components.enemy import Enemy

class Level:
    def parse_level(level):
        """
        Parses the level map, extracts all dynamic entities (coins, enemies), 
        replaces their spawn points with air, and returns the modified collision map and entity lists.
        """
        coins = []
        enemies = []
        # Create a deep copy of the level to modify the tiles, leaving the original map intact
        new_level = [row[:] for row in level] 
        
        for r in range(TILE_ROWS):
            for c in range(TILE_COLS):
                x = c * TILE_SIZE
                y = r * TILE_SIZE

                if new_level[r][c] == Tiles.COIN:
                    # Coin position is center
                    coins.append((x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                    new_level[r][c] = Tiles.AIR
                
                elif new_level[r][c] == Tiles.ENEMY:
                    # Enemy position is top-left
                    enemies.append(Enemy(x, y))
                    new_level[r][c] = Tiles.AIR 
                    
        return new_level, coins, enemies
    
    def draw_level(level):
        """Draws the solid tiles of the level map."""
        for row in range(TILE_ROWS):
            for col in range(TILE_COLS):
                tile_value = level[row][col]
                if tile_value == Tiles.SOLID:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    
                    draw_rectangle(x, y, TILE_SIZE, TILE_SIZE, DARKGRAY)
                    draw_rectangle_lines(x, y, TILE_SIZE, TILE_SIZE, BLACK)