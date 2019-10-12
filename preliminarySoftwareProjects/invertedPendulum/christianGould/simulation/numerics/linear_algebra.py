import numpy as np
import scipy.linalg as la
import scipy.optimize as op
def schur(matrix, **kwargs):
    return eval('la.schur')(matrix, **kwargs)

def inv(matrix, **kwargs):
    return eval('np.linalg.inv')(matrix, **kwargs)

def multi_dot(*args):
    return eval('np.linalg.multi_dot')([*args])

def solve_ricatti_equation(S, A, B, Q, R):
    pass
    #return la.solve(A.T.dot(S) + S.dot(A) - np.linalg.multi_dot([S, B, inv(R), B.T, S]) + Q, np.eye(4))

def CARE(A, B, Q, R):
    '''
    For Visualization Purposes Only
    
    Otherwise We should make an (n x n) matrix
   
    >>> m, n = A.shape
    >>> np.eye(A.shape)

    and copy each element into it, in this method we create multiple python objects unnecessarily 
    ''' 
    top = np.concatenate((A, multi_dot(B, inv(R), B.T)),axis=1)
    bottom = np.concatenate((-Q, -A.T), axis=1)
    hamiltonian = np.vstack([top, bottom])
   
    T1, U1 = schur(hamiltonian, output='real')
    T2, U2 = la.rsf2csf(T1,U1)
   
    # schur Factorization (conceptually)
    #>>> eigs = np.diag(T)[:2]
    #>>> print(np.diag(np.diag(eigs)))

    m, n = U1.shape
    P11 = U1[0:int(m/2), 0:int(n/2)]
    P21 = U1[int(m/2):, 0:int(n/2)]
    #print("1:\n",P11)
    #print("2:\n",P21)

    return P21.dot(inv(P11))


if __name__=='__main__':

#    A = np.array([[-0.995591312646866, -1.249081404879689],
#                  [  0.32005394541192,  1.163391509093344]])
#    
#    B = np.array([[-0.216261377558112],
#                  [ 2.120734989643097]])
#    
#    Q = np.array([[2.60795573245784, 1.26610295835102],
#                  [1.26610295835102, 2.95448749241003]])
#    
#    R = np.array([[0.00137941893917394]])
#
#    LQR(A,B,Q,R)

#    T, U, val= make_hamiltonian(A, B, Q, R, sort='lhp')
#    print(T)
#    print('')
#    print(U)
#    print('Satisfied: ',val)
#    eigs = np.diag(T)[:2]
#    print(np.diag(np.diag(eigs)))
# 
#    m, n = U.shape
#    P11 = U[0:int(m/2), 0:int(n/2)]
#    P21 = U[int(m/2):, 0:int(n/2)]
# 
#    K = P21.dot(inv(P11))
# 
#    print(K)
 
    # Mass Dampener:
    '''
    Mass Dampener System
    '''
    # ( Step 1 ) Define A and B
    A = np.array([[0, 1],
                  [0, -1/5]])
 
    B = np.array([[0],
                  [1]])
 
    # ( Step 2 ) Choose Q and R
 
    Q = np.eye(2)
    R = np.array([[1/100]])
 
    # ( Step 3 ) Solve ARE
    '''
    Continuous Algebraic Riccati Equation:
     A.T.dot(S) + S.dot(A) - np.linalg.multi_dot([S, B, inv(R), B.T, S]) + Q
    '''
    P = CARE(A, B, Q, R)
    print("Solution:\n", P)
    print("Optimal K: \n",multi_dot(inv(R), B.T, P))






