import pygame
from pygame.locals import SRCALPHA
class Box(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups):
        super().__init__(groups)
        self.image = pygame.Surface(size, SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        pygame.draw.rect(self.image, (255, 255, 255),
                         pygame.Rect((0, 0), size), width=2)
        self.old_rect = self.rect.copy()