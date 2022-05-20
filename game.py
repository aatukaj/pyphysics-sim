from enum import Enum, auto
import pygame
from pygame import Vector2
from pygame.locals import *
import pygame.gfxdraw
from line import LineSegment, Polygon
from particle import Particle
from constants import *
import random
from camera import CameraGroup
import pickle
import sys

class State(Enum):
    DEFAULT = auto()
    CREATING_POLYGON = auto()

class App:
    def __init__(self):
        pygame.init()

        self.clock =  pygame.time.Clock()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)

        self.camera_group=CameraGroup()
        self.obstacles = pygame.sprite.Group()
        self.fps = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.state = State.DEFAULT
        self.window_moved = False

        self.UPDATEFPS = USEREVENT+2
        pygame.time.set_timer(self.UPDATEFPS, 100)

        self.prev_point = None      
        LineSegment((100, 700), (500, 700), (self.camera_group, self.obstacles))
        LineSegment((500, 500), (800, 400), (self.camera_group, self.obstacles))

        Polygon([(0, 0), (1500, 0), (1500, 1000), (0, 1000)], (self.camera_group, self.obstacles))

        for _ in range(50):
            Particle((100, 200), (200, 0), 20, self.camera_group, self.camera_group, color=random.choice(list(COLORS.values())))


    def render(self):
        self.win.fill((0, 0, 0))
        self.camera_group.zoomed_draw()
        text_surface = self.font.render(
            f"FPS: {round(self.fps)}", False, (255, 255, 255))
        self.win.blit(text_surface, (0, 0))

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
                self.window_moved = True
            if event.type == WINDOWMOVED:
                self.window_moved = True

            if event.type == KEYDOWN:
                if event.key == K_s:
                    self.save_obstacles() 
                    
                elif event.key == K_w:
                    self.load_obstacles()
            
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
                            LineSegment(self.prev_point, self.mpos, (self.obstacles, self.camera_group))
                        self.prev_point = self.mpos
                        
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
                dt=0

            self.mpos = self.camera_group.screenpos_to_worldpos(Vector2(pygame.mouse.get_pos()))
            self.handle_events()  
            self.handle_mouse()
            self.camera_group.update(dt)
            self.render()


            
if __name__ == "__main__":
    app = App()
    app.run()