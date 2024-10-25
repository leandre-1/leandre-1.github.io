import pygame

class DialogBox:
    def __init__(self, screen, font):
        self.box = pygame.image.load('dialogue/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 150))

    def render (self, screen):
        screen.blit(self.box, (0, 0))