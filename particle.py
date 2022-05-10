import pygame
from pygame import Vector2
from pygame.locals import SRCALPHA
from line import LineSegment
from box import Box
from constants import WIDTH, HEIGHT

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, vel, acc, r, obstacles, groups):
        super().__init__(groups)
        self.image = pygame.Surface((r*2, r*2), SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        pygame.gfxdraw.aacircle(self.image, r, r, r-1, (255, 255, 255))
        pygame.gfxdraw.filled_circle(self.image, r, r, r-1, (255, 255, 255))
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.r = r
        self.obstacles = obstacles
        self.old_rect = self.rect.copy()

    def box_collision(self, box):
        if (self.rect.right >= box.rect.left and self.old_rect.right <= box.old_rect.left):
                        self.rect.right = box.rect.left
                        self.pos.x = self.rect.x
                        self.vel.x *= -1

        if (self.rect.left <= box.rect.right and self.old_rect.left >= box.old_rect.right):
            self.rect.left = box.rect.right
            self.pos.x = self.rect.x
            self.vel.x *= -1

        if (self.rect.bottom >= box.rect.top and self.old_rect.bottom <= box.old_rect.top):
            self.rect.bottom = box.rect.top
            self.pos.y = self.rect.y
            self.vel.y *= -1

        if (self.rect.top <= box.rect.bottom and self.old_rect.top >= box.old_rect.bottom):
            self.rect.top = box.rect.bottom
            self.pos.y = self.rect.y
            self.vel.y *= -1
    
    def line_collision(self, line):
        center = self.pos+Vector2(self.r, self.r)
        point = line.closestPoint(center)
        dist = point.distance_to(center)
        if dist < self.r:
            if point == line.A or point == line.B:
                normal = (line.A-line.B).normalize()
            else:
                normal = Vector2(-(line.A.y-line.B.y),
                                line.A.x-line.B.x).normalize()
            self.vel.reflect_ip(normal)
            dif = center-point
            if dif.x != 0 or dif.y != 0:
                dif.scale_to_length(dist-self.r+3)
                self.pos += dif
                self.rect.topleft = self.pos

    def window_collision(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x
            self.vel.x *= -1
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.pos.x = self.rect.x
            self.vel.x *= -1

        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.y
            self.vel.y *= -1
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.pos.y = self.rect.y
            self.vel.y *= -1

    def collision(self):
        collision_sprites = pygame.sprite.spritecollide(
            self, self.obstacles, False)
        if collision_sprites:
            for sprite in collision_sprites:
                if isinstance(sprite, Box):
                    self.box_collision(sprite)
                if isinstance(sprite, LineSegment):
                    self.line_collision(sprite)
        self.window_collision()

    def update(self, dt):
        self.old_rect = self.rect.copy()

        self.pos.x += self.vel.x * dt
        self.rect.x = round(self.pos.x)
        self.vel.x += self.acc.x * dt
        self.pos.y += self.vel.y * dt
        self.rect.y = round(self.pos.y)
        self.vel.y += self.acc.y * dt
            
        self.collision()
        self.window_collision()
