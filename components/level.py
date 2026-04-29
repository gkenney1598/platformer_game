from pyray import *
from settings import *
from enums import Tiles
from components.cyclops import Cyclops
from components.hay import Hay
from components.sheep import Sheeps, Sheep
from components.vase import Vases, Vase
from components.blocks import Blocks, Grass, Pillar

class Level:

    def parse_level(level):
        """
        Parses the level map, extracts all dynamic entities (coins, enemies), 
        replaces their spawn points with air, and returns the modified collision map and entity lists.
        """
        sheeps = Sheeps()
        cyclops = []
        hay = Hay()
        vases = Vases()
        solid = Blocks()
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
                    hay.collection.append(Rectangle(x, y + TILE_SIZE * 0.3, TILE_SIZE, TILE_SIZE * 0.7))
                    new_level[r][c] = Tiles.AIR

                elif new_level[r][c] == Tiles.SHEEP:
                    sheeps.collection.append(Sheep(x, y))
                    new_level[r][c] = Tiles.AIR

                elif new_level[r][c] == Tiles.BOUNDARY:
                    new_level[r][c] = Tiles.BOUNDARY

                elif new_level[r][c] == Tiles.VASE_EMPTY:
                    vases.collection.append(Vase(x, y, False))
                    new_level[r][c] = Tiles.AIR

                elif new_level[r][c] == Tiles.VASE_FULL:
                    vases.collection.append(Vase(x, y, True))
                    new_level[r][c] = Tiles.AIR

                elif new_level[r][c] == Tiles.SOLID:
                    new_level[r][c] = Tiles.SOLID
                    if r == TILE_ROWS - 1:           
                        solid.collection.append(Grass(x, y))
                    else:
                        solid.collection.append(Pillar(x, y))



        return new_level, sheeps, cyclops, hay, vases, solid
    
    # def draw_level(level):
    #     """Draws the solid tiles of the level map."""
    #     for row in range(TILE_ROWS):
    #         for col in range(TILE_COLS):
    #             tile_value = level[row][col]
    #             if tile_value == Tiles.SOLID:
    #                 x = col * TILE_SIZE
    #                 y = row * TILE_SIZE
                    
    #                 draw_rectangle(x, y, TILE_SIZE, TILE_SIZE, DARKGRAY)
    #                 draw_rectangle_lines(x, y, TILE_SIZE, TILE_SIZE, BLACK)
    