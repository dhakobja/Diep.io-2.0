import pygame

class Screen:
    def __init__(self, width, height, fullscreen=False):
        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        self.screen = self.create_screen()
        pygame.display.set_caption("Diep.io 2.0")
    
    def create_screen(self):
        flags = pygame.DOUBLEBUF
        if self.fullscreen:
            flags |= pygame.FULLSCREEN
        return pygame.display.set_mode((self.width, self.height), flags)
    
    def update_display(self):
        pygame.display.flip()

    def clear_screen(self, color=(0, 0, 0)):
        self.screen.fill(color)

    def get_surface(self):
        return self.screen