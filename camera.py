
import pygame
from pygame import Vector2
from pygame.locals import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector2(0, 0)
        self.zoom_scale = 1
        self.update_vars()

    def update_vars(self):
        display_size=Vector2(self.display_surface.get_size())
        self.half_w, self.half_h = display_size//2

        self.internal_surf_size = display_size*2
        self.internal_surf = pygame.Surface(self.internal_surf_size, SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(
            center=(self.half_w, self.half_h))
        self.internal_offset = pygame.math.Vector2()

        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def change_zoom(self, amount):
        new_zoom = self.zoom_scale+amount
        if new_zoom < 0.5:
            self.zoom_scale = 0.5
        elif new_zoom > 1.5:
            self.zoom_scale = 1.5
        else:
            self.zoom_scale = new_zoom
        
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
            self.internal_surf, self.internal_surf_size * round(self.zoom_scale, 1))
        scaled_rect = scaled_surf.get_rect(
            center=(self.half_w, self.half_h))
        self.display_surface.blit(scaled_surf, scaled_rect)

    def screenpos_to_worldpos(self, pos):
        size = pygame.Vector2(pygame.display.get_window_size())
        return (pos+(size*self.zoom_scale-size)//2)/self.zoom_scale-self.offset

    def update(self, *args, **kwargs):

        keys = pygame.key.get_pressed()
        dt = args[0]
        
        if keys[K_RIGHT]:
            self.offset.x -= 1000*dt
        if keys[K_LEFT]:
            self.offset.x += 1000*dt
        if keys[K_DOWN]:
            self.offset.y -= 1000*dt
        if keys[K_UP]:
            self.offset.y += 1000*dt

        return super().update(*args, **kwargs)

