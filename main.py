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

# Bullet
bullets = []

# Clock to set and track FPS
clock = pygame.time.Clock()
FPS = 60

run = True

def shooting(player, keys):
    if keys[pygame.K_UP]:
        if len(bullets) < 5:
            bullets.append({
                "position": [player.centerx, player.top],
                "original_y": player.top,
                "radius": 10,
                "direction": "up", 
                "bullet_velocity": 10,
                "bullet_range": 200})

def update_bullets():
    for bullet in bullets:
        if bullet["direction"] == "up":
            # Calculate the new position
            new_y = bullet["position"][1] - bullet["bullet_velocity"]

            if abs(new_y - bullet["original_y"]) > bullet["bullet_range"]:
                bullets.remove(bullet)
            else:
                bullet["position"][1] = new_y

def draw_bullets():
    for bullet in bullets:
        pygame.draw.circle(screen, WHITE, bullet["position"], bullet["radius"])

def main():
    global run

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player.x -= 10
        if keys[pygame.K_d]:
            player.x += 10 
        if keys[pygame.K_w]:
            player.y -= 10
        if keys[pygame.K_s]:
            player.y += 10   

        screen.fill(BLACK)     

        pygame.draw.rect(screen, WHITE, player)
        shooting(player, keys)
        update_bullets()
        draw_bullets()

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()