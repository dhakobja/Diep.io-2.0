import pygame
from Bullets.bullets import Bullet

class Player:
    def __init__(self, name, level, position):
        self.name = name
        self.level = level
        self.width = 40
        self.height = 40
        self.speed = 10
        self.position = position
        self.bullets = []
        self.fire_rate = 100
        self.last_shot_time = 0
    
    def move(self, keys):
        if keys[pygame.K_a]:
            self.position[0] -= self.speed
        if keys[pygame.K_d]:
            self.position[0] += self.speed
        if keys[pygame.K_w]:
            self.position[1] -= self.speed
        if keys[pygame.K_s]:
            self.position[1] += self.speed

    def shooting(self, keys):
        current_time = pygame.time.get_ticks()

        directions = {
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right"
        }
        for key, direction in directions.items():
            if keys[key] and current_time - self.last_shot_time > self.fire_rate:
                new_bullet = Bullet(position=self.position.copy(), direction=direction)
                self.bullets.append(new_bullet)
                self.last_shot_time = current_time

    def update_bullets(self, screen):
        self.bullets = [bullet for bullet in self.bullets if not bullet.update()]
        for bullet in self.bullets:
            bullet.draw(screen)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), [self.position[0], self.position[1], self.width, self.height])