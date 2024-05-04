import pygame
import random

class Orb:
    def __init__(self, radius, xp_value, health, position=None):
        self.radius = radius
        self.xp_value = xp_value
        self.health = health
        self.max_health = health # Store the max health to draw the orb health bar

        if position:
            self.position = position
        else:
            self.position = [random.randint(0, 1600), random.randint(0, 1200)]  # Random position on the screen
    
    def draw(self, screen, camera):
        # Apply camera transformation
        adjusted_position = camera.apply(self.position)

        # Draw the orb itself
        pygame.draw.circle(screen, (255, 255, 255), adjusted_position, self.radius)

        # Draw the health bar
        health_bar_length = 40
        health_bar_height = 5
        health_bar_x = adjusted_position[0] - health_bar_length // 2
        health_bar_y = adjusted_position[1] - self.radius - 10

        if self.health < self.max_health:
            pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_length, health_bar_height))
            current_health_length = (self.health / self.max_health) * health_bar_length
            pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_length, health_bar_height))

    def collide_with_bullet(self, bullet):
        # Check the distance between the center of the orb and the bullet position
        distance = pygame.math.Vector2(self.position).distance_to(pygame.math.Vector2(bullet.position))
        return distance < self.radius
    
    def collide_with_player(self, player):
        # Check the distance between the center of the orb and the player position
        distance = pygame.math.Vector2(self.position).distance_to(pygame.math.Vector2(player.position))
        return distance < self.radius + player.width
    
class SmallOrb(Orb):
    def __init__(self, position=None, health=None):
        super().__init__(radius=20, xp_value=60, health=20, position=position)