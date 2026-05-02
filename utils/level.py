from pyray import *
from settings import *
from enums import Tiles, Tiles_Two
from components.cyclops import Cyclopses, Cyclops
from components.hay import Hay
from components.sheep import Sheeps, Sheep
from components.vase import Vases, Vase
from components.environment.blocks import Blocks, Grass, Pillar, Cave_Grass, Stone
from components.environment.fence import Fences, Fence
from components.environment.door import Door
from components.gold import Gold

class Level:
    def parse_level_one(level):
        sheeps = Sheeps()
        cyclopses = Cyclopses()
        hay = Hay()
        vases = Vases()
        solid = Blocks()
        fences = Fences()
        door = None
        # Create a deep copy of the level to modify the tiles, leaving the original map intact
        new_level = [row[:] for row in level] 
        
        #TODO match case
        for r in range(TILE_ROWS):
            for c in range(TILE_COLS):
                x = c * TILE_SIZE
                y = r * TILE_SIZE

                if new_level[r][c] == Tiles.CYCLOPS:
                    # Enemy position is top-left
                    cyclopses.collection.append(Cyclops(x, y))
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

                elif new_level[r][c] == Tiles.FENCE:
                    new_level[r][c] = Tiles.AIR
                    fences.collection.append(Fence(x, y))

                elif new_level[r][c] == Tiles.DOOR:
                    new_level[r][c] == Tiles.AIR
                    door = Door(x, y)
                    
        return new_level, sheeps, cyclopses, hay, vases, solid, fences, door
    
    def parse_level_two(level):

        solid = Blocks()
        cyclopses = Cyclopses()
        vases = Vases()
        gold = Gold()

        # Create a deep copy of the level to modify the tiles, leaving the original map intact
        new_level = [row[:] for row in level] 
        
        #TODO match case
        for r in range(TILE_ROWS):
            for c in range(TILE_COLS):
                x = c * TILE_SIZE
                y = r * TILE_SIZE

                match new_level[r][c]:
                    case Tiles_Two.SOLID:
                        new_level[r][c] = Tiles.SOLID
                        if r == TILE_ROWS - 1:
                            solid.collection.append(Cave_Grass(x,y))  
                        else:
                            solid.collection.append(Stone(x,y))

                    case Tiles_Two.CYCLOPS:
                        new_level[r][c] = Tiles.AIR 
                        cyclopses.collection.append(Cyclops(x,y))
                        
                    case Tiles_Two.BOUNDARY:
                        new_level[r][c] = Tiles.BOUNDARY

                    case Tiles_Two.VASE_EMPTY:
                        vases.collection.append(Vase(x, y, False))
                        new_level[r][c] = Tiles.AIR

                    case Tiles_Two.VASE_FULL:
                        vases.collection.append(Vase(x, y, True))
                        new_level[r][c] = Tiles.AIR

                    case Tiles_Two.GOLD:
                        gold.collection.append(Rectangle(x, y + TILE_SIZE * 0.5, TILE_SIZE * 0.5, TILE_SIZE * 0.5))
                        new_level[r][c] = Tiles.AIR


                                        
        return new_level, solid, cyclopses, vases, gold
    