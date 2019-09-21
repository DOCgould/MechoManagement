import pygame
import math
import numpy as np

#GLOBALS
gravity = np.array([0, 0.002])
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
        if isinstance(obj, Drawable):
            self.objects.append(obj)

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

class MathHelp:
    pass

class Drawable:

    def __init__(self, x=0, y=0, color=(0,0,255)):
        self.pos = np.array([x, y]).astype(float)
        self.vel = np.array([0,0]).astype(float)
        self.color = color

    def act(self):
        pass

    def draw(self, screen):
        pass

class Circle(Drawable):
    
    def __init__(self, x=0, y=0, r=1, color=(0,0,255)):
        super(Circle, self).__init__(x, y, color)
        self.r = r

    def act(self):
        global gravity
        # Apply Gravity
        self.vel += gravity
        self.pos += self.vel
        if (self.pos[1] >= HEIGHT - self.r):
            self.vel[1] = 0
        self.pos[0] = max(0, min(WIDTH, self.pos[0]))
        self.pos[1] = max(0, min(HEIGHT, self.pos[1]))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.r, 1)

class Cart(Drawable):
    
    def __init__(self, x=0, y=0, width=0, height=0, color=(0,0,0), cartMass=50, pendulumLength=100, pendulumMass=10, circleRadius=10):
        super(Cart, self).__init__(x, y, color)
        self.width          = width
        self.height         = height
        self.theta          = 90
        self.cartMass       = cartMass
        self.pendulumLength = pendulumLength
        self.pendulumMass   = pendulumMass
        self.circleRadius   = circleRadius

    def act(self)
        global gravity
        # Apply Gravity
        self.vel += gravity
        # TODO Determine theta_new based on velocity

        # TODO Determine position based on Forces given from pendulum

    def draw(self, screen):
        theta     = math.radians(self.theta)
        endPointx = int(math.cos(theta)*self.pendulumLength + self.pos[0] + self.width/2)
        endPointy = int(self.pos[1] - math.sin(theta)*self.pendulumLength)
        pygame.draw.rect(screen, self.color, (int(self.pos[0]), int(self.pos[1]), 
                            self.width, self.height))
        pygame.draw.line(screen, self.color, (int(self.pos[0] + self.width/2), int(self.pos[1])),
                            (endPointx, endPointy), 3)
        pygame.draw.circle(screen, self.color, (endPointx, endPointy), self.circleRadius)

def main():
    window = Window("Inverted Pendulum")
    width, height = 100,100
    window.addObject(Cart((WIDTH - width)/2, HEIGHT-height, width, height, pendulumLength=200))
    window.run()

if __name__ == "__main__":
    main()
