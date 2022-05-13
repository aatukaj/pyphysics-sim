
import pygame
from pygame import Vector2
from pygame.locals import *
import pygame.gfxdraw
from line import LineSegment
from box import Box
from particle import Particle
from constants import *
import random
from camera import CameraGroup


def main():

    pygame.init()

    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    all_sprites = CameraGroup()
    obstacles = pygame.sprite.Group()
    lines = pygame.sprite.Group()
    Box((375, 250), (50, 400), (all_sprites, obstacles))


    line_groups = (obstacles, all_sprites, lines)
    LineSegment((100, 700), (500, 700), line_groups)
    LineSegment((500, 500), (800, 400), line_groups)
    LineSegment((0, 0), (WIDTH, 0), line_groups)
    LineSegment((0, 0), (0, HEIGHT), line_groups)
    LineSegment((0, HEIGHT), (WIDTH, HEIGHT), line_groups)
    LineSegment((WIDTH, 0), (WIDTH, HEIGHT), line_groups)

    p = Particle((100, 200), (200, 0),
                 20, obstacles, (obstacles, all_sprites), color=(255, 0, 0))
    for _ in range(20):
        Particle((100, 200), (200, 0),
                 20, obstacles, (obstacles, all_sprites), color=random.choice(list(COLORS.values())))

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
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    prev_pos = p.rect.center
                    background.fill((0, 0, 0))
                    draw_path = not draw_path
            if event.type == MOUSEWHEEL:
                all_sprites.zoom_scale += event.y * 0.1
        keys = pygame.key.get_pressed()

        if keys[K_RIGHT]:
            all_sprites.offset.x -= 1000*dt
        if keys[K_LEFT]:
            all_sprites.offset.x += 1000*dt
        if keys[K_DOWN]:
            all_sprites.offset.y -= 1000*dt
        if keys[K_UP]:
            all_sprites.offset.y += 1000*dt
        
        mpos = Vector2(pygame.mouse.get_pos())
        all_sprites.update(dt)
        win.fill((0, 0, 0))
        win.blit(background, (0, 0))
        all_sprites.zoomed_draw()
        win.blit(text_surface, (0, 0))
        #for line in lines:
            #line.A=all_sprites.screenpos_to_worldpos(mpos)

        pygame.display.update()


if __name__ == "__main__":
    main()
