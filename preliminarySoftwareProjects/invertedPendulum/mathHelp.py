import math
import random
import numpy as np
import matplotlib.pylab as plt
import scipy.integrate

def ctrb(A, B):
    """
    The pyton analog of the ctrb function in matlab
    """
    C0 = np.array(B)
    for i in range(1, len(A)):
        tmp = np.dot(np.linalg.matrix_power(A,i), B)
        C0 = np.append(C0, tmp, 1)
    return C0

# Code from Steve Brunton
def cartpend(y, m, M, L, g, d, u):
    Sy = math.sin(y[2])
    Cy = math.cos(y[2])
    D = m*L*L*(M+m*(1-Cy**2))

    dy = [y[1]]
    dy.append((float(1/D))* (-m**2 * L**2 * g * Cy * Sy + m * L**2 * 
                        (m*L*y[3]**2*Sy - d*y[1])) + m * L * L * (float(1/D)) * u)
    dy.append(y[3])
    dy.append((float(1/D)) * ((m+M)*m*g*L*Sy - m*L*Cy*(m*L*y[3]**2*Sy - d*y[1]))
                                - m*L*Cy*(float(1/D))*u + 0.01 * random.uniform(0,1))
    return np.array(dy)
