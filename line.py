from pygame import Vector2
import pygame

import pygame.gfxdraw

class LineSegment(pygame.sprite.Sprite):
    def __init__(self, A, B, groups):
        super().__init__(groups)
        self.A = Vector2(A)
        self.B = Vector2(B)
        
    def draw(self, win, offset = Vector2(0, 0)):
        #pygame.draw.rect(win, (100, 100, 100), self.rect, width=2)
        pygame.draw.line(win, (255, 255, 255), self.A+offset, self.B+offset, width=2)
        pygame.draw.circle(win, (255, 255, 255), self.A+offset, radius=5)
        pygame.draw.circle(win, (255, 255, 255), self.B+offset, radius=5)

    @property
    def rect(self):
        return pygame.Rect(min(self.A.x, self.B.x), min(self.A.y, self.B.y), max(abs(self.A.x-self.B.x), 1), max(abs(self.A.y-self.B.y), 1)) 


    def closestPoint(self, P):
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
    

def main():
    from pygame.locals import QUIT
    line=LineSegment(Vector2(100, 100), Vector2(200, 200), ())
    win = pygame.display.set_mode((500, 500))
    run = True
    while run:
        win.fill((0, 0, 0))
        mpos = Vector2(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
        point = line.closestPoint(mpos)
        pygame.draw.circle(win, (255, 0, 0), point, 5)
        line.draw(win)
        pygame.display.update()

if __name__ == "__main__":
    main()