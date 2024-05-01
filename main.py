import pygame
import sys

pygame.init()

# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Diep.io 2.0")

# Player
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 40
player = pygame.rect.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PLAYER_WIDTH, PLAYER_HEIGHT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.x -= 10
            if event.key == pygame.K_d:
                player.x += 10 
            if event.key == pygame.K_w:
                player.y -= 10
            if event.key == pygame.K_s:
                player.y += 10   

    screen.fill(BLACK)     

    pygame.draw.rect(screen, WHITE, player)
    
    pygame.display.flip()
    