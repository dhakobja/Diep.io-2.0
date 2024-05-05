import pygame
import random

from Bullets.bullets import Bullet

class Player:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.level = 1
        self.xp = 0
        self.max_xp = 100
        self.health = 100
        self.speed = 5
        self.bullets = []
        self.fire_rate = 200
        self.last_shot_time = 0
        self.collision_damage = 10
    
    def move(self, keys, world_width, world_height):
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

        for direction in keys:
            if keys[direction] and current_time - self.last_shot_time > self.fire_rate:
                new_bullet = Bullet(position=[self.position[0] + self.width // 2, self.position[1] + self.height //2], direction=direction)
                self.bullets.append(new_bullet)
                self.last_shot_time = current_time

    def update_bullets(self):
        self.bullets = [bullet for bullet in self.bullets if not bullet.update()]

    def add_xp(self, xp_value):
        self.xp += xp_value
        if self.xp >= self.max_xp:
            self.update_level()
    
    def update_level(self):
        remaining_xp = self.xp % self.max_xp
        self.level += int(self.xp // self.max_xp)
        self.xp = 0 + remaining_xp
        self.max_xp = int(self.max_xp * 1.2)

    def collide_with_player(self, player):
        # Check if the player is colliding with another player
        return (self.position[0] < player.position[0] + player.width and
                self.position[0] + self.width > player.position[0] and
                self.position[1] < player.position[1] + player.height and
                self.position[1] + self.height > player.position[1])
    
    def collide_with_bullet(self, bullet):
        # Check if the player is colliding with a bullet
        return (self.position[0] < bullet.position[0] + bullet.radius and
                self.position[0] + self.width > bullet.position[0] and
                self.position[1] < bullet.position[1] + bullet.radius and
                self.position[1] + self.height > bullet.position[1])

    def draw(self, screen, camera):
        # Draw the player, but apply the camera offset first
        adjusted_position = camera.apply(self.position)
        pygame.draw.rect(screen, (255, 255, 255), [adjusted_position[0], adjusted_position[1], self.width, self.height])

        # Draw the health bar of the Player
        health_bar_length = self.width
        health_bar_height = 5
        health_bar_x = adjusted_position[0]
        health_bar_y = adjusted_position[1] + self.height + 5

        # Background of the health bar (red)
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_length, health_bar_height))

        # Current health (green)
        if self.health > 0:
            current_health_length = (self.health / 100) * health_bar_length
        else:
            current_health_length = 0

        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, current_health_length, health_bar_height))

        # Draw the player level
        font = pygame.font.Font(None, 24)
        level_text = font.render(f"Lvl: {self.level}",True, (255, 255, 255))
        screen.blit(level_text, (adjusted_position[0], adjusted_position[1] - 20))
    
    def draw_player_specifics(self, screen):
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

        # Draw the current player_s xp and max_xp
        xp_font = pygame.font.Font(None, 24)
        xp_text = xp_font.render(f"XP: {self.xp}/{self.max_xp}", True, (255, 255, 255))
        screen.blit(xp_text, (xp_bar_x + 10, xp_bar_y - 20))

class StandardClass(Player):
    def __init__(self, name, world_width=2400, world_height=1800):
        super().__init__()
        self.name = name
        self.position = [random.randint(0, world_width), random.randint(0, world_height)]

class Tank(StandardClass):
    def __init__():
        super().__init__(health=200)