import pygame
import cart
import numpy as np
import sys

if len(sys.argv) > 1:
    controlFlag = int(sys.argv[1])
else:
    controlFlag = 0

(width, height ) = (600,300)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Inverted Pendulum Simulation')

c = cart.cart(
    np.array([-50,0,np.pi + 0.1,0],dtype=np.float64),
    controlled=controlFlag)

pygame.display.flip()
clock = pygame.time.Clock()
running = True
maxFPS = 600
while running:
    clock.tick(maxFPS)
    c.update()
    c.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
