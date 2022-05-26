  
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
        self.MIN_ZOOM = 0.25
        self.MAX_ZOOM = 2

    def update_vars(self):
        display_size=Vector2(self.display_surface.get_size())
        self.half_w, self.half_h = display_size//2

    def change_zoom(self, amount):
        new_zoom = self.zoom_scale+amount
        if new_zoom < self.MIN_ZOOM:
            self.zoom_scale = self.MIN_ZOOM
        elif new_zoom > self.MAX_ZOOM:
            self.zoom_scale = self.MAX_ZOOM
        else:
            self.zoom_scale = new_zoom
        
    
    def optimized_zoomed_draw(self):
         self.display_surface.fill((0, 0, 0))
         for sprite in self.sprites():
            sprite.draw(self.display_surface, offset=self.offset+Vector2(self.half_w, self.half_h)/self.zoom_scale, zoom = self.zoom_scale)


    def screenpos_to_worldpos(self, pos):
        return (pos)/self.zoom_scale-Vector2(self.half_w, self.half_h)/self.zoom_scale-self.offset
        
    def handle_keys(self, dt):
        keys = pygame.key.get_pressed()
        amount = 500*dt*(1/self.zoom_scale)
        if keys[K_RIGHT]:
            self.offset.x -= amount
        if keys[K_LEFT]:
            self.offset.x += amount
        if keys[K_DOWN]:
            self.offset.y -= amount
        if keys[K_UP]:
            self.offset.y += amount

