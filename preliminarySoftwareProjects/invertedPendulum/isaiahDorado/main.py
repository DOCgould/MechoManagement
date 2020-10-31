import pygame
import numpy as np
import math
import scipy.linalg
import sys

(width,height) = (600,480)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Inverted Pendulum')
controlFlag = True  # Control switch: On -> True // Off -> False
g = 9 # gravity

class pendulumCart():
    def __init__(self, state, m=1., M=5., L=25.,controlled=False):
        self.state = state # x position of cart, cart velocity along x axis, angular position, and angular velocity
        self.m = m # mass of pendulum
        self.M = M # mass of cart
        self.L = L # length of pendulum
        self.d = 1 # friction
        self.x = state[0] # x position of the cart
        self.th = state[2] # angle at which the pendulum is pointing

        # Cart Information
        self.cartwidth = 50 #cart width
        self.cartheight = 25 #cart height
        self.cartX = (self.cartwidth / 2)
        self.cartY = self.cartheight / 2

        # Pendulum Information
        self.penLen = 25
        self.th = math.pi
        self.penX = self.cartX + self.penLen * math.sin(self.th)
        self.penY = self.cartY - self.penLen * math.cos(self.th)
        self.penR = 10

        self.dt = 0.016

        # If the controlFlag is True, optimize K value, if not, zero the matrix
        if controlled:
            self.K = optimizeK(self.m, self.M, self.L, g, self.d) 
        else: 
            self.K = np.zeros(4)

    def drawOnScreen(self,screen):
        # Function to draw inverted pendulum in pygame window
        centerX = width/2
        centerY = height/2

        pygame.draw.rect(screen, (0,255,0),(centerX + self.x, centerY - self.cartheight, self.cartwidth,self.cartheight))
        pygame.draw.line(screen, (0,0,255), (centerX + self.cartX, centerY-self.cartY),(centerX + self.penX, centerY-self.penY), 3)
        pygame.draw.circle(screen, (255,0,0),(int(centerX + self.penX),int(centerY - int(self.penY))), int(self.penR))

    def update(self):
        # Function to update inverted pendulum values
        self.state = rk4(self.dt,self.state,self.m,self.M,self.L,g,self.d,
        np.dot(-self.K,(self.state - np.array([0,0,np.pi,0])))) 
        self.x = self.state[0]
        self.th = self.state[2]
        self.cartX = self.x + (self.cartwidth / 2)
        self.penX = self.cartX + 50 * np.sin(self.th)
        self.penY = self.cartY - 50 * np.cos(self.th)

def rk4(dt, state, m,M,L,g,d,u):
    # ODE solver
    k1 = dt * stateDiff(state,m,M,L,g,d,u)
    k2 = dt * stateDiff(state+(k1/2),m,M,L,g,d,u)
    k3 = dt * stateDiff(state+(k2/2),m,M,L,g,d,u)
    k4 = dt * stateDiff(state+k3, m,M,L,g,d,u)
    return state + (k1 + 2 * k2 + 2 * k3 + k4) / 6

def optimizeK(m, M, L, g, d):
    # Function to find the optimal K matrix
    s = 1.
    A = np.matrix([[0,1,0,0], [0,-d/M, -m*g/M,0], [0,0,0,1], [0,-s*d/(M*L), -s*(m+M)*g/(M*L),0]], dtype=np.float64)

    B = np.matrix([[0],[1/M],[0],[s/(M*L)]],dtype=np.float64)
    Q = np.matrix([[1,0,0,0], [0,1,0,0], [0,0,10,0], [0,0,0,100]], dtype=np.float64)

    R = np.matrix([0.001],dtype=np.float64)
    temp = scipy.linalg.solve_continuous_are(A,B,Q,R)
    K = scipy.linalg.inv(R) * B.T * temp
    return K

def stateDiff(state,m,M,L,g,d,u):
    # Function that performs differential equations for the inverted pendulum
    dy = np.zeros(4,dtype=np.float64)
    Sy = np.sin(state[2])
    Cy = np.cos(state[2])
    D = m * L * L * (M + m * (1 - Cy**2))

    dy[0] = state[1]
    dy[1] = (1 / D) * (-(m**2) * (L**2) * g * Cy * Sy + m * (L**2) * (m * L * state[3]**2 * Sy - d * state[1])) + m * L * L * (1 / D) * u
    dy[2] = state[3]
    dy[3] = (1 / D) * ((m + M) * m * g * L * Sy - m * L * Cy * (m * L * (state[3]**2) * Sy - d * state[1])) - m * L * Cy * (1 / D) * u
    return dy

if __name__ == "__main__":
    m, M, L, g, d = 1, 5, 2, -10, 1
    K = optimizeK(m,M,L,g,d)
  
class Environment: # Create the pygame environment
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = (0,0,0)

env = Environment(width,height)
cart = pendulumCart(np.array([-50,0,np.pi + 0.1,0], dtype=np.float64), controlled=controlFlag)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    
    screen.fill(env.color)
    cart.update()
    cart.drawOnScreen(screen)
    pygame.display.flip()