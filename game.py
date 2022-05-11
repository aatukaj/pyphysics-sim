
import pygame
from pygame import Vector2
from pygame.locals import *
import pygame.gfxdraw
from line import LineSegment
from box import Box
from particle import Particle
from constants import *


def main():
    pygame.init()

    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    all_sprites = pygame.sprite.Group()

    obstacles = pygame.sprite.Group()
    lines = pygame.sprite.Group()
    Box((375, 250), (50, 400), (all_sprites, obstacles))

    line = LineSegment((100, 100), (200, 400), (obstacles, lines))
    LineSegment((500, 500), (800, 400), (obstacles, lines))
    p = Particle((100, 200), (800, 0),
                 20, obstacles, (obstacles, all_sprites), color=(255, 0, 0))
    for _ in range(10):
        Particle((100, 200), (800, 0),
                 20, obstacles, (obstacles, all_sprites))

    prev_pos = p.rect.center

    run = True
    background = pygame.Surface((WIDTH, HEIGHT))

    # path update timer
    UPDATEPATH = USEREVENT+1
    pygame.time.set_timer(UPDATEPATH, 1)

    # fps update timer
    draw_path = False
    UPDATEFPS = USEREVENT+2
    pygame.time.set_timer(UPDATEFPS, 100)

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = font.render(
        f"FPS: {round(clock.get_fps())}", False, (255, 255, 255))

    while run:
        dt = clock.tick()/1000/3
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == UPDATEPATH:
                if draw_path:
                    pos = p.rect.center
                    pygame.draw.aaline(background, (255, 0, 0), prev_pos, pos)
                    prev_pos = pos
            if event.type == UPDATEFPS:
                fps = clock.get_fps()
                text_surface = font.render(
                    f"FPS: {round(fps)}", False, (255, 255, 255))
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    prev_pos = p.rect.center
                    background.fill((0, 0, 0))
                    draw_path = not draw_path
        keys = pygame.key.get_pressed()

        if keys[K_RIGHT]:
            line.A.x += 1000*dt
            line.B.x += 1000*dt
        if keys[K_LEFT]:
            line.A.x -= 1000*dt
            line.B.x -= 1000*dt
        if keys[K_DOWN]:
            line.A.y += 1000*dt
            line.B.y += 1000*dt
        if keys[K_UP]:
            line.A.y -= 1000*dt
            line.B.y -= 1000*dt

        all_sprites.update(dt)

        win.fill((0, 0, 0))
        win.blit(background, (0, 0))
        win.blit(text_surface, (0, 0))
        for line in lines:
            line.draw(win)
        all_sprites.draw(win)

        pygame.display.update()


if __name__ == "__main__":
    main()
