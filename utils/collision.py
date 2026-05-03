from pyray import *

class Collision:
    def check_collection(player, collectables):
        collected_indices = []
        
        for i, collect in enumerate(collectables.collection):
            
            if check_collision_recs(player.rect, collect) and is_key_pressed(KeyboardKey.KEY_F):
                collected_indices.append(i)
                
        return collected_indices
    
    def check_collision(player, entities):
        
        for i, entity in enumerate(entities):

            if check_collision_recs(player.bounding_box, entity.rect):
                return i
                              
        return -1