import numpy as np
import scipy.linalg as la
import pygame
import math
import sys


from numerics.integrators import *
from numerics.linear_algebra import CARE
from simulation_environment import *

# Constants
# -- COLOR
BLACK=(  0,   0,   0)
GREEN=(  0, 255,   0)
BLUE =(  0,   0, 255)
RED = (255,   0,   0)

# -- SCREEN
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 600

CENTER=(int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))
LEFT=(int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))
RIGHT=(int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))

# -- FUNCTION DEFINITONS

def LQR(A,B,Q,R):
    return la.solve_continuous_are(A, B, Q, R)

def optimal_k_calculation(A, B, Q, R, control_switch=1):

    P1 = CARE(A,B,Q,R) # Optimal P Matrix
    #print("CARE: \n",P1)
    P2 = LQR(A,B,Q,R)
    #print("LQR: \n",P2)
    K = np.linalg.multi_dot([la.inv(R), B.T, P2]) # Optimal Matrix Multiplication
    return control_switch*K



if __name__ == "__main__":
    import sys
    import time
    
    Header='''
    Thanks For Checking Out this Pendulum!
    -- --------------------------------------------------
    Here are some Configuration Flags Run Like This
    ```
    $ python3 main.py # This is Uncontrolled Pendulum 

    $ python3 main.py 1 # This is Controlled Upwards
    
    $ python3 main.py -1 # This is Controlled Downwards
    ```
    Enjoy
    --Christian
    '''
    # Initializations
    # -- Environment
    print(Header);

    running = True
    background_color = BLACK
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('CART MAIN')

    # -- Characteristics
    # Starting Cart Position ( Centered )

    cart_position = CENTER
    cart_size = (100,25)
    x_pos, y_pos = cart_position 
    
    # Initialization Sequence:
    #     1) put the cart on the 'track'
    cart = Cart(screen, cart_position, cart_size, GREEN)

    #     2) put the pendulum on the cart
    pendulum = Pendulum(screen, rod_position=cart_position)
   
    m = 1 # Bob mass
    M = 5 # Cart mass
    L = 2 # Pole Length 
    g = -10 # Gravity 
    d = 1 # Dampening

    s = 1 # Control Direction up=1 or down=-1
    control_switch = 0 # Control Switch 0:off 1:on

    stepsize = .01
    
    y_vec = np.array([[x_pos], [0], [np.pi-np.pi/2.8], [0]])
    #y_vec = np.array([[x_pos], [0], [np.pi-.2], [0]])
    desired = np.array([[x_pos], [0], [np.pi], [0]])
    
    # -- USER INPUT
    # -- ---------------------------------------------------

    if len(sys.argv)>=2:
        s = int(sys.argv[1])
    
        if s == -1: # Control Down
            control_switch = 1;
            y_vec = desired#np.array([[x_pos], [0], [np.pi], [.001]]) 
            desired = np.array([[x_pos], [0], [0], [0]])

        if s == 1: # Control Up
            control_switch = 1;
        
    
    # -- LINEARIZED EQUATIONS OF MOTION
    # -- ---------------------------------------------------
    A = np.array([[ 0,          1,                0, 0],
                  [ 0,       -d/M,           -m*g/M, 0],
                  [ 0,          0,                0, 1],
                  [ 0, -s*d/(M*L), -s*(m+M)*g/(M*L), 0]])

    B = np.array([[        0],
                  [      1/M],
                  [        0],
                  [s*1/(M*L)]])

    Q = np.array([[1, 0,  0,   0],
                  [0, 1,  0,   0],
                  [0, 0, 10,   0],
                  [0, 0,  0, 100]])
    
    R = np.array([[.01]])
    
    # -- CALCULATE OPTIMAL K MATRIX
    # -- ---------------------------------------------------
    
    K = optimal_k_calculation(A, B, Q, 
                                 R, control_switch);    
    
    # -- ITERATION
    # -- ---------------------------------------------------
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BLACK)

        # CALCULATE U
        u = (-K).dot(y_vec - desired)
        
        # CALCULATE DELTA-T
        y_vec = HeunsMethod('equations_of_motion', y_vec, stepsize,
                                                m,     M,        L, 
                                                g,     d,        u)
        # UPDATE VECTORS
        new_x = y_vec[0][0] 
        new_theta = y_vec[2][0]

        # UPDATE SIMULATION
        cart.update_pos( new_x, y_pos )
        pendulum.update_pos(new_theta, cart.cart_position, cart.cart_size) 
 
        # UPDATE SCREEN
        pygame.display.flip()
