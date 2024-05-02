import pygame

class Bullet:
    def __init__(self, position, direction):
        self.position = position
        self.original_position = position.copy()
        self.radius = 10
        self.direction = direction
        self.velocity = 10
        self.damage = 10
        self.range = 500

    def update(self):
        # Move bullet based on direction
        if self.direction == "up":
            self.position[1] -= self.velocity
        elif self.direction == "down":
            self.position[1] += self.velocity
        elif self.direction == "left":
            self.position[0] -= self.velocity
        elif self.direction == "right":
            self.position[0] += self.velocity

        # Check if bullet has exceeded its range
        if abs(self.position[1] - self.original_position[1]) > self.range or abs(self.position[0] - self.original_position[0]) > self.range:
            return True  # Bullet should be deleted
        return False  # Bullet is still active
    
    def draw(self, screen, position):
        pygame.draw.circle(screen, (255, 255, 255), position, self.radius)