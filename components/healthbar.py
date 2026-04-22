from pyray import *

class HealthBar:
    def __init__(self, max_health, x, y, width, height):
        self.max_health = max_health
        self.current_health = max_health
        self.bar_width = width
        self.bar_height = height # Top-left corner of the bar
        self.bar_rect = Rectangle(x, y, self.bar_width, self.bar_height)
        self.health_rect = Rectangle(x, y, self.bar_width, self.bar_height)

    def update(self, x, y):
        self.bar_rect.x = x
        self.bar_rect.y = y
        self.health_rect.x = x
        self.health_rect.y = y

    def update_health(self, new_health):
        self.current_health = max(0, min(new_health, self.max_health)) 
        self.health_rect.width = (self.current_health / self.max_health) * self.bar_width 

    def draw(self):
        # Draw background (gray)
        draw_rectangle_rec(self.bar_rect, GRAY)
        
        # Draw foreground (green)
        draw_rectangle_rec(self.health_rect, GREEN)