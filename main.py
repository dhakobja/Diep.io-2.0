import pygame

from Screen.screen import Screen
from Players.player import Player
from Orbs.orbs import SmallOrb
from Camera.camera import Camera

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.screen = Screen(800, 600).screen
        self.player = Player("Player 1", 1, [400, 300])
        self.orbs = [SmallOrb() for _ in range(5)]
        self.camera = Camera(self.player, 800, 600)
        self.run = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.shooting(keys)
        self.update_orbs()
        self.camera.update()
    
    def update_orbs(self):
        for orb in self.orbs[:]:
            for bullet in self.player.bullets[:]:
                if orb.collide_with_bullet(bullet):
                    self.player.bullets.remove(bullet)
                    orb.health -= bullet.damage
                    if orb.health <= 0:
                        self.player.add_xp(orb.xp_value)
                        self.orbs.remove(orb)
                        self.orbs.append(SmallOrb())
                        break
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen, self.camera)
        self.player.update_bullets(self.screen, self.camera)
        for orb in self.orbs:
            orb.draw(self.screen, self.camera.apply(orb.position))
        pygame.display.flip()
    
    def run_game(self):
        while self.run:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
        pygame.quit()

def main():
    game = Game()
    game.run_game()

if __name__ == "__main__":
    main()