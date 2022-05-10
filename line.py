from pygame import Vector2
import pygame

import pygame.gfxdraw

class LineSegment(pygame.sprite.Sprite):
    def __init__(self, A, B, groups):
        super().__init__(groups)
        self.A = A
        self.B = B
        self.rect=pygame.Rect(min(self.A.x, self.B.x), min(self.A.y, self.B.y), abs(self.A.x-self.B.x), abs(self.A.y-self.B.y))
        self.old_rect=self.rect.copy()
    def draw(self, win):
        #pygame.draw.rect(win, (100, 100, 100), self.rect, width=2)
        pygame.draw.aaline(win, (255, 255, 255), self.A, self.B)


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