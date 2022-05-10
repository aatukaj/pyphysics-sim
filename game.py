
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

    LineSegment(Vector2(100, 100), Vector2(200, 400), (obstacles, lines)),
    LineSegment(Vector2(500, 500), Vector2(800, 400), (obstacles, lines))
    p = Particle(Vector2(100, 200), Vector2(800, 0),
                 Vector2(0, 1000), 20, obstacles, all_sprites)
    Particle(Vector2(100, 200), Vector2(800, 0),
             Vector2(0, 1000), 20, obstacles, all_sprites)

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
    fps = 0
    text_surface = font.render(
        f"FPS: {round(clock.get_fps())}", False, (255, 255, 255))

    while run:
        dt = clock.tick()/1000
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
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    prev_pos = p.rect.center
                    background.fill((0, 0, 0))
                    draw_path = not draw_path
        keys = pygame.key.get_pressed()

        if keys[K_RIGHT]:
            p.vel.x += 1000*dt
        if keys[K_LEFT]:
            p.vel.x -= 1000*dt
        if keys[K_DOWN]:
            p.vel.y += 1000*dt
        if keys[K_UP]:
            p.vel.y -= 1500*dt

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
