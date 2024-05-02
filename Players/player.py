import pygame
from Bullets.bullets import Bullet

class Player:
    def __init__(self, name, level, position):
        self.name = name
        self.level = level
        self.xp = 0
        self.max_xp = 100
        self.width = 40
        self.height = 40
        self.speed = 5
        self.position = position
        self.bullets = []
        self.fire_rate = 200
        self.last_shot_time = 0
    
    def move(self, keys, screen, world_width, world_height):
        # Calculate potential new positions
        dx = self.speed if keys[pygame.K_d] else -self.speed if keys[pygame.K_a] else 0
        dy = self.speed if keys[pygame.K_s] else -self.speed if keys[pygame.K_w] else 0

        # Apply new position with boundary constraints of the game world
        new_x = max(0, min(world_width - self.width, self.position[0] + dx))
        new_y = max(0, min(world_height - self.height, self.position[1] + dy))

        # Update the player's position
        self.position = [new_x, new_y]

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
                new_bullet = Bullet(position=[self.position[0] + self.width // 2, self.position[1] + self.height //2], direction=direction)
                self.bullets.append(new_bullet)
                self.last_shot_time = current_time

    def update_bullets(self, screen, camera):
        self.bullets = [bullet for bullet in self.bullets if not bullet.update()]
        for bullet in self.bullets:
            bullet.draw(screen, camera.apply(bullet.position))

    def add_xp(self, xp_value):
        self.xp += xp_value
        if self.xp >= 100:
            self.update_level()
    
    def update_level(self):
        self.level += self.xp // 100
        self.xp = 0

    def draw(self, screen, camera):
        # Draw the player, but apply the camera offset first
        adjusted_position = camera.apply(self.position)
        pygame.draw.rect(screen, (255, 255, 255), [adjusted_position[0], adjusted_position[1], self.width, self.height])

        # Draw the player level
        font = pygame.font.Font(None, 24)
        level_text = font.render(f"Lvl: {self.level}",True, (255, 255, 255))
        screen.blit(level_text, (adjusted_position[0], adjusted_position[1] - 20))

        # Draw the xp Bar    
        xp_bar_length = screen.get_width()
        xp_bar_height = 5
        xp_bar_x = 0
        xp_bar_y = screen.get_height() - xp_bar_height 

        # Background of the xp bar (red)
        pygame.draw.rect(screen, (255, 0, 0), (xp_bar_x, xp_bar_y, xp_bar_length, xp_bar_height))
    
        # Current XP (green)
        if self.max_xp > 0:  # To avoid division by zero
            current_xp_length = (self.xp / self.max_xp) * xp_bar_length
        else:
            current_xp_length = 0
        pygame.draw.rect(screen, (0, 255, 0), (xp_bar_x, xp_bar_y, current_xp_length, xp_bar_height))