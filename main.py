from collections.abc import Iterable
import pygame

from Players.player import Player
from Orbs.Orbs import SmallOrb

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Diep.io 2.0")
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.player = Player("Player 1", 1, [400, 300])
        self.orbs = [SmallOrb() for _ in range(5)]
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
        self.player.draw(self.screen)
        self.player.update_bullets(self.screen)
        for orb in self.orbs:
            orb.draw(self.screen)
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