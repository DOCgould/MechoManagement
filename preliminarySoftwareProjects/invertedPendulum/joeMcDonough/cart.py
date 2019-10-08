import numpy as np 
import pygame
import scipy.linalg

g = -10

#TODO: (Low Priority) Make it so that user can grab and move the pendulum
class cart():
    """A class for simulating the inverted pendulum on a cart system.

    Attributes:
        state (np.array(4)): Contains the x position, x velocity, 
            angular position, and angular velocity of the system
        m (float): mass of the pendulum
        M (float): mass of the cart
        L (float): length of pendulum
        d (float): friction
        controlled (bool): flag to simulate uncontrolled or controlled system
    """
    def __init__(self, state, m=1., M=5., L=25.,controlled=False):
        self.state = state
        self.m = m
        self.M = M
        self.L = L
        self.d = 1.
        self.x = state[0]
        self.th = state[2]

        # Cart Data
        self.cw = 50 #cart width
        self.ch = 25 #cart height
        self.cx = self.x + (self.cw / 2)
        self.cy = self.ch / 2

        # Pendulum Data
        self.px = self.cx + 50 * np.sin(self.th)
        self.py = self.cy - 50 * np.cos(self.th)
        self.pr = 10
    
        self.dt = .016

        if controlled:
            self.K = getOptimalK(self.m,self.M,self.L,g,self.d) 
        else: 
            self.K = np.zeros(4)

    def draw(self,screen):
        """Draw cart-pendulum on pygame screen"""
        w,h = screen.get_size()
        center = w/2

        pygame.draw.rect(
            screen, (255,0,0),
            (center + self.x, h/2 - self.ch, self.cw,self.ch))
        pygame.draw.line(
            screen, (255,0,0), 
            (center + self.cx,h/2-self.cy),(center + self.px,h/2-self.py), 3)
        pygame.draw.circle(
            screen, (255,0,0), 
            (int(center + self.px),h/2 - int(self.py)), int(self.pr))
  
    def update(self):
        """Updates the internal state of the cart-pendulum system"""
        self.state = rk4(self.dt,self.state,self.m,self.M,self.L,g,self.d,
        np.dot(-self.K,(self.state - np.array([0,0,np.pi,0])))) 
        self.x = self.state[0]
        self.th = self.state[2]
        self.cx = self.x + (self.cw / 2)
        self.px = self.cx + 50 * np.sin(self.th)
        self.py = self.cy - 50 * np.cos(self.th)

def getOptimalK(m,M,L,g,d):
    """Find optimal K matrix using LQR"""
    s = 1.
    A = np.matrix([
        [0,1,0,0],
        [0,-d/M, -m*g/M,0],
        [0,0,0,1],
        [0,-s*d/(M*L), -s*(m+M)*g/(M*L),0]],dtype=np.float64)

    B = np.matrix([[0],[1/M],[0],[s/(M*L)]],dtype=np.float64)

    Q = np.matrix([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,10,0],
        [0,0,0,100]],dtype=np.float64)

    R = np.matrix([0.001],dtype=np.float64)
    #TODO: Implement my own ARE solver??
    tmp = scipy.linalg.solve_continuous_are(A,B,Q,R)
    K = scipy.linalg.inv(R)*B.T*tmp
    return K

def heuns(dt, state,m,M,L,g,d,u):
    """Numerical ode solver using heun's method.
    returns updated state after one time step
    """
    ye = state + dt*stateDiff(state,m,M,L,g,d,u)
    updated = state + (dt/2)*(stateDiff(state,m,M,L,g,d,u) 
        + stateDiff(ye,m,M,L,g,d,u))
    return updated

def rk4(dt, state, m,M,L,g,d,u):
    """Numerical ode solver using Runge Kutta method.
    returns updated state after one time step
    """
    k1 = dt*stateDiff(state,m,M,L,g,d,u)
    k2 = dt*stateDiff(state+(k1/2),m,M,L,g,d,u)
    k3 = dt*stateDiff(state+(k2/2),m,M,L,g,d,u)
    k4 = dt*stateDiff(state+k3, m,M,L,g,d,u)
    return state + (k1 + 2*k2 + 2*k3 + k4)/6

def stateDiff(state,m,M,L,g,d,u):
    """ Calculate the differential for inverted pendulum on a cart 
    given a state. Returns as numpy array
    """
    dy = np.zeros(4,dtype=np.float64)
    Sy = np.sin(state[2])
    Cy = np.cos(state[2])
    D = m*L*L*(M+m*(1-Cy**2))

    dy[0] = state[1]
    dy[1] = (1/D)*(-(m**2)*(L**2)*g*Cy*Sy 
        + m*(L**2)*(m*L*state[3]**2*Sy - d*state[1])) + m*L*L*(1/D)*u
    dy[2] = state[3]
    dy[3] = (1/D)*((m+M)*m*g*L*Sy 
        - m*L*Cy*(m*L*(state[3]**2)*Sy - d*state[1])) - m*L*Cy*(1/D)*u

    return dy

if __name__ == "__main__":
    m, M, L, g, d = 1., 5., 2., -10., 1.
    K = getOptimalK(m,M,L,g,d)