import pygame
from pygame import Rect, Vector2
from line import LineSegment

from constants import *
from math import pi

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, vel, r, obstacles, groups, color=(255, 255, 255), acc=GRAVITY):
        super().__init__(groups)
        self.rect = Rect(pos, (r*2, r*2))
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.acc = Vector2(acc)
        self.r = r
        self.mass = pi*self.r**2
        self.obstacles = obstacles
        self.old_rect = self.rect.copy()
        self.has_collided = False
        self.color = color
    
    def line_collision(self, line: LineSegment):
        center = self.rect.center
        point = line.closestPoint(center)
        if not point: return
        dist = point.distance_to(center)
        if dist < self.r:
            #if point == line.A or point == line.B:
                #normal = (line.A-line.B).normalize()
            #else:
            normal = Vector2(-(line.A.y-line.B.y),
                                line.A.x-line.B.x).normalize()
            self.vel.reflect_ip(normal)
            dif = center-point
            if dif.x != 0 or dif.y != 0:
                dif.scale_to_length(dist-self.r)
                self.pos -= dif
                self.rect.topleft = self.pos

    def particle_collision(self, other):
        if other.has_collided:
            return
        c1 = Vector2(self.rect.center)
        c2 = Vector2(other.rect.center)
        if c1.distance_to(c2) > self.r+other.r:
            return
        m1 = self.mass
        m2 = other.mass
        v1 = self.vel.copy()
        v2 = other.vel.copy()
        try:
            self.vel = self.vel-((2*m2)/(m1+m2))*((v1-v2).dot(c1-c2)/(c1-c2).magnitude()**2)*(c1-c2)
            other.vel = other.vel-((2*m1)/(m1+m2))*((v2-v1).dot(c2-c1)/(c2-c1).magnitude()**2)*(c2-c1)
            dif = c1-c2
            dif.scale_to_length(c1.distance_to(c2)-self.r-other.r)
            self.pos-=dif
            self.rect.topleft = self.pos
        except ZeroDivisionError:
            self.pos += Vector2(0, self.r+other.r)
            self.rect.topleft = other.pos
 
        self.has_collided = True
        
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
                if sprite == self:
                    continue
                if isinstance(sprite, LineSegment):
                    self.line_collision(sprite)
                if isinstance(sprite, Particle):
                    self.particle_collision(sprite)

    def update(self, dt):
        self.has_collided= False
        self.old_rect = self.rect.copy()

        self.pos += self.vel *dt
        self.vel += self.acc * dt

        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)
            
        self.collision()
    def draw(self, win, offset=Vector2(0, 0), zoom = 1):
        pygame.draw.circle(win, self.color, (Vector2(self.rect.center)+offset)*zoom, self.r*zoom)
