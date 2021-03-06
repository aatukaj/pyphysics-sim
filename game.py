import pygame
from pygame import Vector2
from pygame.locals import *
import pygame.gfxdraw
import pygame_gui as pgg


from line import LineSegment, Polygon
from particle import Particle
from camera import CameraGroup
from constants import *
from ui import MenuWindow

import random
import pickle
import sys
from enum import Enum, auto


class State(Enum):
    DEFAULT = auto()
    CREATING_POLYGON = auto()



class App:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
        

        self.camera_group = CameraGroup()
        self.obstacles = pygame.sprite.Group()
        self.fps = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.state = State.DEFAULT
        self.window_moved = False
        self.time_scale = 1

        self.UPDATEFPS = USEREVENT+2
        pygame.time.set_timer(self.UPDATEFPS, 100)

        self.prev_point = None
        LineSegment((100, 700), (500, 700),
                    (self.camera_group, self.obstacles))
        LineSegment((500, 500), (800, 400),
                    (self.camera_group, self.obstacles))

        Polygon([(0, 0), (1500, 0), (1500, 1000), (0, 1000)],
                (self.camera_group, self.obstacles))

        for _ in range(30):
            Particle((100, 200), (200, 0), 20, self.camera_group,
                     self.camera_group, color=random.choice(list(COLORS.values())))
        
        self.manager = pgg.UIManager((self.win.get_size()))
        self.menu_window = MenuWindow(self.manager, self)

    def render(self):
        self.win.fill((0, 0, 0))
        self.camera_group.optimized_zoomed_draw()
        text_surface = self.font.render(
            f"FPS: {round(self.fps)}", False, (255, 255, 255))
        self.win.blit(text_surface, (0, 0))
        self.manager.draw_ui(self.win)
        pygame.display.update()

    def handle_mouse(self):
        mouse = pygame.mouse.get_pressed()
        if self.state == State.DEFAULT:
            if mouse[0]:
                if self.grabbed_point is None:
                    for obstacle in self.obstacles:
                        if self.mpos.distance_to(obstacle.A) < 30:
                            self.grabbed_point = obstacle.A
                            break
                        elif self.mpos.distance_to(obstacle.B) < 30:
                            self.grabbed_point = obstacle.B
                            break
                else:
                    self.grabbed_point.xy = self.mpos

            else:
                self.grabbed_point = None

            if mouse[2]:
                for obstacle in self.obstacles:
                    if self.mpos.distance_to(obstacle.closestPoint(self.mpos)) < 10:
                        obstacle.kill()

    def handle_events(self):
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.UPDATEFPS:
                self.fps = self.clock.get_fps()
            if event.type == MOUSEWHEEL:
                self.camera_group.change_zoom(event.y * 0.1)
            if event.type == VIDEORESIZE:
                self.camera_group.update_vars()
                self.manager.set_window_resolution((self.win.get_size()))
                self.window_moved = True
            if event.type == WINDOWMOVED:
                self.window_moved = True

            if event.type == KEYDOWN:
                if event.key == K_s:
                    self.save_obstacles()

                elif event.key == K_w:
                    self.load_obstacles()
                elif event.key == K_SPACE:
                    if self.time_scale != 0:
                        self.time_scale = 0
                    else: self.time_scale = 1
                elif event.key == K_LALT:
                    if not self.menu_window.alive():
                        self.menu_window = MenuWindow(self.manager, self)
                    else:
                        self.menu_window.kill()

            if self.state == State.DEFAULT:
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        self.state = State.CREATING_POLYGON
                        self.prev_point = None

            elif self.state == State.CREATING_POLYGON:
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        self.state = State.DEFAULT

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.prev_point is not None:
                            LineSegment(self.prev_point, self.mpos,
                                        (self.obstacles, self.camera_group))
                        self.prev_point = self.mpos
                        
            self.manager.process_events(event)

    def save_obstacles(self):
        self.camera_group.remove(self.obstacles)
        self.saved_obstacles = pickle.dumps(self.obstacles)
        self.camera_group.add(self.obstacles)

    def load_obstacles(self):
        self.camera_group.remove(self.obstacles)
        self.obstacles.empty()
        self.obstacles = pickle.loads(self.saved_obstacles)
        self.camera_group.add(self.obstacles)

    def run(self):
        while True:
            dt = self.clock.tick()/1000
            if self.window_moved:
                self.window_moved = False
                dt = 0

            self.screen_mpos = Vector2(pygame.mouse.get_pos())
            self.mpos = self.camera_group.screenpos_to_worldpos(self.screen_mpos)
            self.handle_events()
            self.manager.update(dt)

            if not self.menu_window.get_container().rect.collidepoint(self.screen_mpos):
                self.handle_mouse()
            self.camera_group.update(dt*self.time_scale)
            self.camera_group.handle_keys(dt)
            self.render()

if __name__ == "__main__":
    app = App()
    app.run()
