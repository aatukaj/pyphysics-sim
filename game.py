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
import pickle

def main():

    pygame.init()

    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)

    all_sprites = CameraGroup()
    obstacles = pygame.sprite.Group()
    saved_obstacles = pickle.dumps(obstacles)
    #Box((375, 250), (50, 400), (all_sprites, obstacles))

    line_groups = (obstacles)

    LineSegment((100, 700), (500, 700), line_groups)
    LineSegment((500, 500), (800, 400), line_groups)

    Polygon([(0, 0), (1500, 0), (1500, 1000), (0, 1000)], line_groups)

    for _ in range(50):
        Particle((100, 200), (200, 0),
                 20, all_sprites, (all_sprites), color=random.choice(list(COLORS.values())))
    
    saved_obstacles = pickle.dumps(obstacles)
    all_sprites.add(obstacles)



    # fps update timer
    UPDATEFPS = USEREVENT+2
    pygame.time.set_timer(UPDATEFPS, 100)

    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = font.render(
        f"FPS: {round(clock.get_fps())}", False, (255, 255, 255))
    run = True
    while run:
        dt = clock.tick(60)/1000
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
            if event.type == KEYDOWN:
                if event.key == K_s:
                    all_sprites.remove(obstacles)
                    saved_obstacles=pickle.dumps(obstacles)
                    all_sprites.add(obstacles)
                elif event.key == K_w:
                    all_sprites.remove(obstacles)
                    obstacles.empty()
                    obstacles = pickle.loads(saved_obstacles)
                    all_sprites.add(obstacles)


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
            for obstacle in obstacles:
                if mpos.distance_to(obstacle.A) < 30:
                    obstacle.A.x = mpos.x
                    obstacle.A.y = mpos.y
                    break
                if mpos.distance_to(obstacle.B) < 30:
                    obstacle.B.x = mpos.x
                    obstacle.B.y = mpos.y
                    break

        all_sprites.update(dt)
        win.fill((0, 0, 0))
        all_sprites.zoomed_draw()
        win.blit(text_surface, (0, 0))

        pygame.display.update()


if __name__ == "__main__":
    main()
