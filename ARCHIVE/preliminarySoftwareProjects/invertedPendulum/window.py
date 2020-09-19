import pygame
import math
import numpy as np
import scipy

from mathHelp import *

#GLOBALS
gravity = -10
d = 1
WIDTH, HEIGHT = 1280, 720

class Window:
    
    def __init__(self, title):
        self.objects = []
        self.background_color = (255, 255, 255)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(self.background_color)
        pygame.display.set_caption(title)

    def exitEvent(self):
        pass

    def addObject(self, obj):
        if isinstance(obj, Drawable): self.objects.append(obj)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.background_color)
            for obj in self.objects:
                obj.act()
                obj.draw(self.screen)
            pygame.display.flip()

        self.exitEvent()

class Drawable:

    def __init__(self, x=0, y=0, color=(0,0,255)):
        self.pos = np.array([x, y]).astype(float)
        self.vel = np.array([0,0]).astype(float)
        self.color = color

    def act(self):
        pass

    def draw(self, screen):
        pass

class InvertedPendulumCart(Drawable):
    
    def __init__(self, y, m, M, L, width, height, color=(0,0,0)):
        self.yPos = 400
        self.circleRadius = 5
        self.y = y
        self.m = m
        self.M = M
        self.L = L
        self.width = width
        self.height = height
        self.color = color
        t0 = 0
        t_bound = 10000
        fun = lambda t, y : cartpend(y, m, M, L, gravity, d, 0)
        self.solver = scipy.integrate.RK45(fun, t0, self.y, t_bound, max_step=0.015)

    def act(self):
        self.solver.step()
        self.y = self.solver.y

    def draw(self, screen):
        theta     = self.y[2]
        endPointx = int(math.sin(theta)*self.L + self.y[0] + self.width/2)
        endPointy = int(self.yPos + math.cos(theta)*self.L)
        pygame.draw.rect(screen, self.color, (int(self.y[0]), int(self.yPos), 
                            self.width, self.height))
        pygame.draw.line(screen, self.color, (int(self.y[0] + self.width/2), int(self.yPos)),
                            (endPointx, endPointy), 3)
        pygame.draw.circle(screen, self.color, (endPointx, endPointy), self.circleRadius)

def main():
    window = Window("Inverted Pendulum")
    width, height = 50,50
    # Constants for the inverted pendulum
    m = 1
    M = 5
    L = 60
    y = np.array([500, 0, np.pi, .5])

    window.addObject(InvertedPendulumCart(y, m, M, L, width, height))
    window.run()

if __name__ == "__main__":
    main()
