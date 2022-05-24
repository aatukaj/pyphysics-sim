  
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

    def change_zoom(self, amount):
        new_zoom = self.zoom_scale+amount
        if new_zoom < 0.25:
            self.zoom_scale = 0.25
        elif new_zoom > 2:
            self.zoom_scale = 2
        else:
            self.zoom_scale = new_zoom
        
    
    def optimized_zoomed_draw(self):
         self.display_surface.fill((0, 0, 0))
         for sprite in self.sprites():
            sprite.draw(self.display_surface, offset=self.offset+Vector2(self.half_w, self.half_h)/self.zoom_scale, zoom = self.zoom_scale)


    def screenpos_to_worldpos(self, pos):
        return (pos)/self.zoom_scale-Vector2(self.half_w, self.half_h)/self.zoom_scale-self.offset
        

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

