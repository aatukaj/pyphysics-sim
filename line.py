from pygame import Vector2
import pygame

import pygame.gfxdraw

class LineSegment(pygame.sprite.Sprite):
    def __init__(self, A, B, groups):
        super().__init__(groups)
        if isinstance(A, Vector2):
            self.A = A
        else: self.A = Vector2(A)
        if isinstance(B, Vector2):
            self.B = B
        else: self.B = Vector2(B)
        
    def draw(self, win, offset = Vector2(0, 0), zoom = 1):
        #pygame.draw.rect(win, (100, 100, 100), self.rect, width=2)
        pygame.draw.line(win, (255, 255, 255), (self.A+offset)*zoom, (self.B+offset)*zoom, width=max(round(2*zoom), 1))
        for p in (self.A, self.B):
            pygame.draw.circle(win, (255, 255, 255), (p+offset)*zoom, radius=7*zoom)


    @property
    def rect(self):
        return pygame.Rect(min(self.A.x, self.B.x), min(self.A.y, self.B.y), max(abs(self.A.x-self.B.x), 1), max(abs(self.A.y-self.B.y), 1)) 


    def closestPoint(self, P):
        if self.A.xy == self.B.xy: return 

        AP = P-self.A
        AB = self.B-self.A
        magnitudeAB = AB.length_squared()
        ABAPproduct = AP.dot(AB)
        distance = ABAPproduct/ magnitudeAB
        if distance < 0:
            return self.A
        elif distance > 1:
            return self.B
        else:
            return self.A+AB*distance
    

class Polygon:
    def __init__(self, points, groups, closed=True):
        self.lines = [LineSegment(points[0], points[1], groups)]
        
        for i in range(2, len(points)):
            self.lines.append(LineSegment(self.lines[-1].B, Vector2(points[i]), groups))
        if closed:
            self.lines.append(LineSegment(self.lines[-1].B, self.lines[0].A, groups))