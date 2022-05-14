
import pygame
from pygame import Vector2
from pygame.locals import *
import pygame.gfxdraw
from line import LineSegment, Polygon
from box import Box
from particle import Particle
from constants import *
import random
from camera import CameraGroup
import time

def main():

    pygame.init()

    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)

    all_sprites = CameraGroup()
    obstacles = pygame.sprite.Group()
    lines = pygame.sprite.Group()
    Box((375, 250), (50, 400), (all_sprites, obstacles))

    line_groups = (obstacles, all_sprites, lines)

    LineSegment((100, 700), (500, 700), line_groups)
    LineSegment((500, 500), (800, 400), line_groups)

    Polygon([(0, 0), (1500, 0), (1500, 1000), (0, 1000)], line_groups)

    for _ in range(20):
        Particle((100, 200), (200, 0),
                 20, obstacles, (obstacles, all_sprites), color=random.choice(list(COLORS.values())))



    # fps update timer
    UPDATEFPS = USEREVENT+2
    pygame.time.set_timer(UPDATEFPS, 100)

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = font.render(
        f"FPS: {round(clock.get_fps())}", False, (255, 255, 255))
    run = True
    while run:
        dt = clock.tick()/1000
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == UPDATEFPS:
                fps = clock.get_fps()
                text_surface = font.render(
                    f"FPS: {round(fps)}", False, (255, 255, 255))
            if event.type == MOUSEWHEEL:
                all_sprites.change_zoom(event.y * 0.1)
            if event.type == VIDEORESIZE:
                all_sprites.update_vars()
                pygame.display.update()

        keys = pygame.key.get_pressed()

        if keys[K_RIGHT]:
            all_sprites.offset.x -= 1000*dt
        if keys[K_LEFT]:
            all_sprites.offset.x += 1000*dt
        if keys[K_DOWN]:
            all_sprites.offset.y -= 1000*dt
        if keys[K_UP]:
            all_sprites.offset.y += 1000*dt

        mouse = pygame.mouse.get_pressed()
        mpos = all_sprites.screenpos_to_worldpos(Vector2(pygame.mouse.get_pos()))
        if mouse[0]:
            for line in lines:
                if mpos.distance_to(line.A) < 30:
                    line.A = mpos
                if mpos.distance_to(line.B) < 30:
                    line.B = mpos

        all_sprites.update(dt)
        win.fill((0, 0, 0))
        all_sprites.zoomed_draw()
        win.blit(text_surface, (0, 0))

        pygame.display.update()


if __name__ == "__main__":
    main()
