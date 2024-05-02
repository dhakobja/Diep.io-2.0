import pygame

class Orb:
    def __init__(self, position, radius, xp_value):
        self.position = position
        self.radius = radius
        self.xp_value = xp_value
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius)

    def collide_with_bullet(self, bullet):
        # Check the distance between the center of the orb and the bullet position
        distance = pygame.math.Vector2(self.position).distance_to(pygame.math.Vector2(bullet.position))
        return distance < self.radius
    
class SmallOrb(Orb):
    def __init__(self, position):
        super().__init__(position, radius=20, xp_value=10)