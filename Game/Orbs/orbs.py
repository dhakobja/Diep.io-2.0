import pygame
from pygame.sprite import Sprite

import random
import uuid

class Orb(Sprite):
    def __init__(self, radius, xp_value, health, position=None, *groups):
        self.id = str(uuid.uuid4())
        self.radius = radius
        self.xp_value = xp_value
        self.health = health
        self.max_health = health # Store the max health to draw the orb health bar

        if position:
            self.position = position
        else:
            self.position = [random.randint(0, 1600), random.randint(0, 1200)]  # Random position on the screen
        
        # Add the orb to the groups
        self._layer = 3
        super().__init__(*groups)

    def draw(self, screen, camera):
        # Apply camera transformation
        adjusted_position = camera.apply(self.position)

        # Draw the orb itself
        pygame.draw.circle(screen, (255, 255, 255), adjusted_position, self.radius)

        # Draw the health bar
        health_bar_length = self.radius * 2
        health_bar_height = 5
        health_bar_x = adjusted_position[0] - health_bar_length // 2
        health_bar_y = adjusted_position[1] - self.radius - 12

        if self.health < self.max_health:
            pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_length, health_bar_height))
            current_health_length = (self.health / self.max_health) * health_bar_length
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_length, health_bar_height))

    def collide_with_bullet(self, bullet):
        # Check the distance between the center of the orb and the bullet position
        distance = pygame.math.Vector2(self.position).distance_to(pygame.math.Vector2(bullet.position))
        return distance < self.radius
    
    def collide_with_player(self, player):
        # Find the closest point on the rectangle to the center of the circle
        closest_x = max(player.position[0], min(self.position[0], player.position[0] + player.width))
        closest_y = max(player.position[1], min(self.position[1], player.position[1] + player.height))

        # Calculate the distance between this closest point and the center of the circle
        distance_x = self.position[0] - closest_x
        distance_y = self.position[1] - closest_y

        # If the distance is less than the radius, there's a collision
        distance = (distance_x**2 + distance_y**2)**0.5
        return distance < self.radius
    
class SmallOrb(Orb):
    def __init__(self, position=None, health=None, *groups):
        super().__init__(10, 60, 20, position, *groups)
        self.contact_damage = 10
        self.group = groups

class MediumOrb(Orb):
    def __init__(self, position=None, health=None, *groups):
        super().__init__(20, 120, 50, position, *groups)
        self.contact_damage = 25
        self.group = groups

class LargeOrb(Orb):
    def __init__(self, position=None, health=None, *groups):
        super().__init__(30, 160, 100, position, *groups)
        self.contact_damage = 50
        self.group = groups