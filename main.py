import pygame
from Players.player import Player

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

    # Game loop
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Process keys
        keys = pygame.key.get_pressed()
        player.move(keys)
        current_time = pygame.time.get_ticks()  # Get current time for shooting management
        player.shooting(keys, current_time)  # Pass current time to shooting

        # Draw everything
        screen.fill(BLACK)
        player.draw(screen)
        player.update_bullets(screen)

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()