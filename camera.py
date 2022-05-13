
import pygame
from pygame import Vector2
from pygame.locals import *
from constants import WIDTH, HEIGHT


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.offset = Vector2(0, 0)
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.zoom_scale = 1
        self.internal_surf_size = (WIDTH*2, HEIGHT*2)
        self.internal_surf = pygame.Surface(self.internal_surf_size, SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(
            center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()

        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def draw(self, win):
        for sprite in self.sprites():
            if hasattr(sprite, "image"):
                offset_pos = sprite.rect.topleft + self.offset
                win.blit(sprite.image, offset_pos)
            else:
                sprite.draw(win, offset=self.offset)

    def zoomed_draw(self):
        self.internal_surf.fill((0, 0, 0))
        for sprite in self.sprites():
            if hasattr(sprite, "image"):
                offset_pos = sprite.rect.topleft + self.offset+self.internal_offset
                self.internal_surf.blit(sprite.image, offset_pos)
            else:
                sprite.draw(self.internal_surf,
                            offset=self.offset+self.internal_offset)

        scaled_surf = pygame.transform.scale(
            self.internal_surf, self.internal_surface_size_vector * round(self.zoom_scale, 1))
        scaled_rect = scaled_surf.get_rect(
            center=(self.half_w, self.half_h))
        self.display_surface.blit(scaled_surf, scaled_rect)

    def screenpos_to_worldpos(self, pos):
        size = pygame.Vector2(pygame.display.get_window_size())
        return (pos+(size*self.zoom_scale-size)//2)/self.zoom_scale+self.offset
