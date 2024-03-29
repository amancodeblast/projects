import numpy as np
import scipy
from scipy import optimize
# K could be removed 
def PnP_reprojection_error(PnP_List, World_points, image_points, K): 
    '''
    Input:

    PnP_List: (12,)
    World_points: len of (N,(4,))
    image_points:len of (N,(2,))
    K: len of 3,3
    Output:
    total_error: len 92
    '''
    P = np.reshape(PnP_List, (3,4))
    total_error = []
    I = np.identity(3)
    for i in range(len(World_points)):
        X_proj_src = np.dot(np.dot(I,P), World_points[i])
        X_proj_src = X_proj_src/X_proj_src[2]
        err_src_x = image_points[i][0] - X_proj_src[0]
        err_src_y = image_points[i][1] - X_proj_src[1]
        err_src = err_src_x**2 + err_src_y**2
        total_error.append(err_src)
    
    return total_error

def NonlinearPnP(P, World_points, image_points, K):
    '''
    input:
    P: (3,4)
    World_points: len 92, (4,)
    image_points: len (92, (2,))
    K: Len of 3,3
    Output:
    optimized_PnP_mat: (3,4)
    final_PnP_mat:  (3,4)
    '''
    PnP_list = np.reshape(P, (12))
    optimized_param_list = scipy.optimize.least_squares(PnP_reprojection_error, PnP_list, args = [World_points, image_points, K])
    optimized_PnP_list = optimized_param_list.x # (12,) and Objects(12,)

    optimized_PnP_mat = np.reshape(optimized_PnP_list, (3,4))    # 3X4
    # After this could be common for linear and non linear as both differs only how they calculate the 
    rot_init = optimized_PnP_mat[:,0:3]
    K_Rot_PnP = np.dot(np.linalg.inv(K), rot_init)

    U,D,V = np.linalg.svd(K_Rot_PnP)
    R_PnP = np.dot(U,V)
    T_PnP = (np.dot(np.linalg.inv(K),optimized_PnP_mat[:,3]))/D[0]
    
    final_PnP_mat = np.zeros([3,4])
    final_PnP_mat[:,0:3] = R_PnP
    final_PnP_mat[:,3] = T_PnP
    
    return optimized_PnP_mat, final_PnP_mat #