import numpy
import time
import math
import random
import pygame
import scipy
import itertools

#Constants
screen = pygame.display.set_mode((width, height))

#-----------------HELPER FUNCTIONS---------------#
def cartpend(y, m, M, L, g, d):
    Sy = math.sin(y[2])
    Cy = math.cos(y[2])
    D = m*L*L*(M+m*(1-Cy**2))

    dy = y[1]
    dy.append(float(1/D)*(-m**2 * L**2*g*Cy*Sy + m*L**2*(m*L*y[3]**2*Sy - d*y[1])) 
            + m*L*L*float(1/D)*u)
    dy.append(y[3])
    dy.append(float(1/D)*((m+M)*m*g*L*Sy - m*L*Cy*(m*L*y[3]**2*Sy - d*y[1]))
            - m*L*Cy*float(1/D)*u + 0.01 * random.uniform(0,1))

    return np.array(dy)

def ctrb(A, B):
    Co = np.array(B)
    for n in range(1, len(A)):
        temp = np.dot(np.linalg.matrix_power(A, n), B)
        Co.append(temp)

def rk4(fun, t0, y0, t_bound, max_step):
    return scipy.integrate.RK45(fun, t0, y0, t_bound, max_step)
    ###CREATE INTEGRATOR####


#------------------CART AND PENDULUM-----------------#
class inverted_pend_cart:
    def __init__(self, state, m, M, L, d):
        self.state = state
        self.x_pos = state[0]
        self.theta = state[2]
        self.width = 100
        self.height = 75
        
        self.pend_x = 
        self.pend_y
        self.m = m
        self.M = M
        self.L = L
        self.g = g
        self.d = d
        self.color = (0,100,100)


    def display(self):
        pygame.draw.rect(screen, self.color, pygame.Rect((self.x,self.y), (self.width,self.height)), 0)

    def move(self):


if __name__ == "__main__":

    my_cart = cart()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0,0,0))
        my_cart.move()
        my_cart.display()
        pygame.display.flip()

