import pygame

from Players.player import Player
from Orbs.Orbs import SmallOrb

def main():
    pygame.init()

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Screen
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Diep.io 2.0")

    # Clock to set and track FPS
    clock = pygame.time.Clock()
    FPS = 60

    # Initialize player
    player = Player("Player 1", 1, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])

    # Initialize orbs
    orbs = [SmallOrb([400, 300])]

    # Game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Process keys
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.shooting(keys)

        # Draw everything
        screen.fill(BLACK)
        player.draw(screen)
        player.update_bullets(screen)
        
        for orb in orbs[:]:
            orb.draw(screen)
            for bullet in player.bullets[:]:
                if orb.collide_with_bullet(bullet):
                    player.bullets.remove(bullet)
                    orb.health -= bullet.damage
                    if orb.health <= 0:
                        orbs.remove(orb)
                        break

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()