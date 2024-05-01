import pygame

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

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player.x -= 1
    if keys[pygame.K_d]:
        player.x += 1 
    if keys[pygame.K_w]:
        player.y -= 1
    if keys[pygame.K_s]:
        player.y += 1   

    screen.fill(BLACK)     

    pygame.draw.rect(screen, WHITE, player)
    
    pygame.display.flip()

pygame.quit()
    