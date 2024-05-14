import pygame
from pygame.sprite import Sprite

class XpDrawings(Sprite):
    def __init__(self, *groups):
        self._layer = 2
        super().__init__(*groups)
        
    def draw_upgrades_available(self, screen, upgrades_available):
        # Draw the upgrades available
        if upgrades_available > 0:
            upgrade_font = pygame.font.Font(None, 24)
            upgrade_text = upgrade_font.render(f"Upgrades: {upgrades_available}", True, (255, 255, 255))
            screen.blit(upgrade_text, (0, 0))

            rect_width = 150
            rect_height = 22
            gap = 6 # Gap between the upgrades

            for i, upgrade  in enumerate(["health", "collision_damage", "speed", "fire_rate"], 1):
                y_pos = 20 * i + gap * i
                upgrade_text = upgrade_font.render(f"{upgrade}", True, (255, 255, 255))
                # Draw a rectangle for the upgrade
                pygame.draw.rect(screen, (255, 255, 255), (0, y_pos, rect_width, rect_height), 2, 5)
                # Center the text inside the rectangle
                text_x = (rect_width - upgrade_text.get_width()) // 2
                text_y = y_pos + (rect_height - upgrade_text.get_height()) // 2
                screen.blit(upgrade_text, (text_x, text_y))
    
    def draw_player_xp_bar(self, screen, max_xp, xp):
        # Draw the xp Bar    
        xp_bar_length = screen.get_width()
        xp_bar_height = 5
        xp_bar_x = 0
        xp_bar_y = screen.get_height() - xp_bar_height 

        # Background of the xp bar (red)
        pygame.draw.rect(screen, (255, 0, 0), (xp_bar_x, xp_bar_y, xp_bar_length, xp_bar_height))
    
        # Current XP (green)
        if max_xp > 0:  # To avoid division by zero
            current_xp_length = (xp / max_xp) * xp_bar_length
        else:
            current_xp_length = 0
        pygame.draw.rect(screen, (0, 255, 0), (xp_bar_x, xp_bar_y, current_xp_length, xp_bar_height))

        # Draw the current player_s xp and max_xp
        xp_font = pygame.font.Font(None, 24)
        xp_text = xp_font.render(f"XP: {xp}/{max_xp}", True, (255, 255, 255))
        screen.blit(xp_text, (xp_bar_x + 10, xp_bar_y - 20))