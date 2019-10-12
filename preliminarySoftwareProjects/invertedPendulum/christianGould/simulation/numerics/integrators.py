import numpy as np
import scipy as sp

def feval(funcName, *args):
    return eval(funcName)(*args)

def HeunsMethod(func, y_vec, h, *args):
    predictor = y_vec + h*eval(func)(y_vec, *args)
    corrector = y_vec + (h/2)*(eval(func)(y_vec, *args) + eval(func)(predictor, *args) )
    return corrector

def equations_of_motion( y_vec, m, M, L, g, d , control=0):
    dy = np.zeros([4,1])
    Sy = np.sin(y_vec[2][0]);
    Cy = np.cos(y_vec[2][0]);
    D = m*L*L*(M+m*(1-Cy**2));

    #  x'    =    Ax   # + Bu
    dy[0][0] = y_vec[1][0]
    dy[1][0] = (1/D)*(-m**2*L**2*g*Cy*Sy + m*L**2*(m*L*y_vec[3][0]**2*Sy - d*y_vec[1][0])) + (m*L*L)*(1/D)*control
    dy[2][0] = y_vec[3][0]
    dy[3][0] = (1/D)*((m+M)*m*g*L*Sy - m*L*Cy*(m*L*y_vec[3][0]**2*Sy - d*y_vec[1][0])) - (m*L*Cy)*(1/D)*control

    # return x' #
    return dy

