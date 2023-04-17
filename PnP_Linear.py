import numpy as np

def create_rows(world_point, image_point):
    rows_per_point = []
    X = world_point[0]
    Y = world_point[1]
    Z = world_point[2]
    x = image_point[0]
    y = image_point[1]
    row1 = (X, Y, Z, 1, 0, 0, 0, 0, -x*X, -x*Y, -x*Z, -x)
    row2 = (0, 0, 0, 0, X, Y, Z, 1, -y*X, -y*Y, -y*Z, -y)
    rows_per_point.append(row1) # adding 1X12
    rows_per_point.append(row2) # adding 1X12
    return rows_per_point # 2X12


def LinearPnP(common_6world_points, common_6image_points, K):
    '''
    Input: 
    common_6world_points:len 6,4 
    common_6image_points: len 6,2
    K: len of 3,3
    Output: 
    PnP_Matrix: (3,4)
    PnP_undecomposed: (3,4)

    '''
    A_PnP = []
    for i in range(len(common_6world_points)):
        rows = create_rows(common_6world_points[i], common_6image_points[i])
        A_PnP.append(rows) # adding all the six points with i one by one so i X row(2X12)
    A_PnP = np.asarray(A_PnP)   # Converting 6X2X12 to numpy of same shape  

    A_PnP = np.reshape(A_PnP,(A_PnP.shape[0]*A_PnP.shape[1],12)) # reshaping numpy to 12 X12 
    U_PnP, S_PnP, V_PnP = np.linalg.svd(A_PnP) # u = (12 X 12), S = (12,) and V = (12X12) # you could also replace u and s by _ _ 
    PnP_elements = V_PnP[-1] # taking the last row of V_transpose (12,)
    PnP_Mat = [[PnP_elements[0], PnP_elements[1], PnP_elements[2], PnP_elements[3]],
                  [PnP_elements[4], PnP_elements[5], PnP_elements[6], PnP_elements[7]],
                  [PnP_elements[8], PnP_elements[9], PnP_elements[10], PnP_elements[11]]] # 3X4
    # This could be done using : PnP_Mat = np.reshape(PnP_elements,(3,4))
    PnP_Mat = np.asarray(PnP_Mat) #3X4

    rot_init = PnP_Mat[:,0:3] # 3 X 3 Getting roration for K_inv multiplication from this
    gamma_R = np.dot(np.linalg.inv(K), rot_init)# 3X3

    U,D,V = np.linalg.svd(gamma_R) # U = (3X3), D = (3,), V = (3,3)
    R_PnP = np.dot(U,V) #3X3
    gamma = D[0] # number 
    #print('gamma', gamma)
    T_PnP = np.matmul(np.linalg.inv(K),PnP_Mat[:,3])/gamma
    # Getting the matrix from Rotation and Translation 
    PnP_Matrix = np.zeros_like(PnP_Mat)
    PnP_Matrix[:,0:3] = R_PnP# PnP matrix = (3X4) and  rotation matrix =(3X3)
    PnP_Matrix[:,3] = T_PnP # PnP Matrix = (3X4) and Translation matrix = (3,)
    #print('PnP Matrix multiplied by K\n',np.dot(K,PnP_Matrix))
    PnP_undecomposed = PnP_Mat # 3X4
    return PnP_undecomposed, PnP_Matrix