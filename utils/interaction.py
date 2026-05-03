from pyray import *
from utils.collision import Collision
from enums import PlayerState, CyclopsState

class Interaction:
    def handle_collection(player, collectable):
        collected_indices = Collision.check_collection(player, collectable)
        if collected_indices:
            for index in sorted(collected_indices, reverse=True):
                collectable.collection.pop(index)
                return 1
        return 0
    
    def handle_vase_interaction(player, vases):
        collided_vase = Collision.check_collision(player, vases.collection)
        if collided_vase >= 0 and is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT) and vases.collection[collided_vase].full:
            if not player.is_sheep:
                vases.collection[collided_vase].full = False
                return 3
            else:
                player.state = PlayerState.SHEEP_BLEET
        return 0
    
    def handle_cyclops_interaction(player, delta_time, cyclopses):
        collided_enemy = Collision.check_collision(player, cyclopses.collection)
        if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
            player.state = PlayerState.ATTACKING
        if is_key_pressed(KeyboardKey.KEY_Q) and player.can_special_attack:
            player.state = PlayerState.SPECIAL_ATTACK
        if collided_enemy != -1 and cyclopses.collection[collided_enemy].state != CyclopsState.DEAD:
            if cyclopses.collection[collided_enemy].boss:
                if is_key_released(KeyboardKey.KEY_Q):
                    cyclopses.collection[collided_enemy].health -= 10
            else: 
                if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
                        cyclopses.collection[collided_enemy].health -= 25
            player.health -= cyclopses.collection[collided_enemy].attack(delta_time)