import numpy as np

def EssentialMatrixFromFundamentalMatrix(F, K):
    '''

    Essential Matrix from Fundamental matrix
    # F: (3,3)
    # K: 3,3 length list
    '''
    # change this to numpy array
    K1 = K.copy()
    K_tranpose = np.transpose(K1) # this becomes the numpy array 
    E = np.dot(np.dot(K_tranpose, F), K) # numpy array (3,3) use @
    # lowering the rank of the matrix 
    U_ess, S_ess, V_ess = np.linalg.svd(E)
    print('singular values of E',S_ess) # singular values of E [1.46523832e+01 1.43276803e+01 6.66519278e-15]
    S_ess[0] = 1
    S_ess[1] = 1
    S_ess[2] = 0
    S_ess2 = np.diag(S_ess)
    E_new = np.dot(np.dot(U_ess, S_ess2), V_ess) # (U_ess@S_ess2)@V_ess
    #print('rank of E', np.linalg.matrix_rank(E_new))
    return E_new # (3,3)
