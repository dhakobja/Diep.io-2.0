import pygame

class Orb:
    def __init__(self, position, radius, xp_value, health):
        self.position = position
        self.radius = radius
        self.xp_value = xp_value
        self.health = health
        self.max_health = health # Store the max health to draw the orb health bar
    
    def draw(self, screen):
        # Draw the orb itself
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius)
        
        # Draw the health bar
        health_bar_length = 40  # Length of the health bar in pixels
        health_bar_height = 5   # Height of the health bar
        health_bar_x = self.position[0] - health_bar_length // 2
        health_bar_y = self.position[1] - self.radius - 10  # Offset by 10 pixels above the orb
        
        # Background of the health bar (red)
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_length, health_bar_height))
        
        # Current health (green)
        current_health_length = (self.health / self.max_health) * health_bar_length
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_length, health_bar_height))

    def collide_with_bullet(self, bullet):
        # Check the distance between the center of the orb and the bullet position
        distance = pygame.math.Vector2(self.position).distance_to(pygame.math.Vector2(bullet.position))
        return distance < self.radius
    
class SmallOrb(Orb):
    def __init__(self, position):
        super().__init__(position, radius=20, xp_value=10, health=100)