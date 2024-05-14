import pygame
from pygame.sprite import Sprite
import random

from Bullets.bullets import Bullet
from Menu.menu import XpDrawings

class Player(Sprite):
    def __init__(self, world_width=2400, world_height=1800, *groups):
        self.world_width = world_width
        self.world_height = world_height
        self.width = 40
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.alpha = 255 # Fully opaque (visible)

        # Bullets
        self.bullets = []
        self.last_shot_time = 0

        # Xp and level
        self.level = 1
        self.xp = 0
        self.max_xp = 100
        self.upgrades_available = 0

        # Upgradable stats
        self.health = 100
        self.speed = 5
        self.fire_rate = 200
        self.collision_damage = 10

        # Call the parent class (Sprite) constructor
        self._layer = 1
        Sprite.__init__(self, *groups)
        self.group = groups
        print("StandardClass group: ", self.group)

        # Initialize the drawing menu
        self.menu = XpDrawings(self.group)

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
    
    def calculate_max_xp_for_level(self, level):
        # Initial max_xp at level 1 is 100
        max_xp = 100
        for i in range(1, level):
            max_xp *= 1.2
        return int(max_xp)
    
    def update_level(self):
        remaining_xp = self.xp % self.max_xp
        self.level += int(self.xp // self.max_xp)
        self.xp = 0 + remaining_xp
        self.max_xp = self.calculate_max_xp_for_level(self.level)
    
    def calculate_upgrades_available_and_draw(self, screen):
        # Calculate the number of upgrades available based on the player's level
        self.upgrades_available = self.level // 2

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
        #pygame.draw.rect(screen, (255, 255, 255), [adjusted_position[0], adjusted_position[1], self.width, self.height])
        self.image.fill((255, 255, 255))
        screen.blit(self.image, (adjusted_position[0], adjusted_position[1]))

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
        # Draw the player's xp bar and total and current xp
        self.menu.draw_player_xp_bar(screen, self.max_xp, self.xp)

        #Draw the player's available upgrades
        self.menu.draw_upgrades_available(screen, self.upgrades_available,)

        # Draw the player's available upgrades
        self.calculate_upgrades_available_and_draw(screen)

    def respawn(self, world_width, world_height):
        # Apply penalties, such as reducing the level
        self.level = max(1, self.level // 2)
        self.xp = 0
        self.health = 100  # Reset health
        self.position = [random.randint(0, world_width), random.randint(0, world_height)]
        self.max_xp = self.calculate_max_xp_for_level(self.level) # Calculate the max_xp based on the new level
    
class StandardClass(Player):
    def __init__(self, name, *group):
        super().__init__(2400, 1800, *group)
        self.name = name
        self.position = [random.randint(0, self.world_width), random.randint(0, self.world_height)]

class Tank(StandardClass):
    def __init__():
        super().__init__(health=200)