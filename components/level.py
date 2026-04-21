from pyray import *
from settings import *
from enums import Tiles
from components.cyclops import Cyclops
from components.hay import Hay
from components.sheep import Sheep
from components.vase import Vase

class Level:
    def parse_level(level):
        """
        Parses the level map, extracts all dynamic entities (coins, enemies), 
        replaces their spawn points with air, and returns the modified collision map and entity lists.
        """
        sheep = []
        cyclops = []
        hay = []
        vase = []
        # Create a deep copy of the level to modify the tiles, leaving the original map intact
        new_level = [row[:] for row in level] 
        
        for r in range(TILE_ROWS):
            for c in range(TILE_COLS):
                x = c * TILE_SIZE
                y = r * TILE_SIZE

                # if new_level[r][c] == Tiles.COIN:
                #     # Coin position is center
                #     coins.append((x + TILE_SIZE / 2, y + TILE_SIZE / 2))
                #     new_level[r][c] = Tiles.AIR
                
                if new_level[r][c] == Tiles.CYCLOPS:
                    # Enemy position is top-left
                    cyclops.append(Cyclops(x, y))
                    new_level[r][c] = Tiles.AIR 

                elif new_level[r][c] == Tiles.HAY:
                    hay.append(Hay(x, y))
                    new_level[r][c] = Tiles.AIR

                elif new_level[r][c] == Tiles.SHEEP:
                    sheep.append(Sheep(x, y))
                    new_level[r][c] = Tiles.AIR

                elif new_level[r][c] == Tiles.BOUNDARY:
                    new_level[r][c] = Tiles.BOUNDARY

                elif new_level[r][c] == Tiles.VASE_EMPTY:
                    vase.append(Vase(x, y, False))
                    new_level[r][c] = Tiles.AIR

                elif new_level[r][c] == Tiles.VASE_FULL:
                    vase.append(Vase(x, y, True))
                    new_level[r][c] = Tiles.AIR


                    
        return new_level, sheep, cyclops, hay, vase
    
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
