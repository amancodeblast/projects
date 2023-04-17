import numpy as np
def LinearTriangulation(inlsrc_pts, inldst_pts, P, P_dash, K):
    '''
    inlsrc_pts: List of 463,2
    inldst_pts: List of 463,2
    P: (3,4)
    P_dash: (4, 3, 4)
    K: (3,3) len list

    Output: 
    World_points: length(462,2)

    '''
    World_points = []
    P = np.dot(K,P)
    P_dash = np.dot(K,P_dash)
    P_dash_row1 = P_dash[0]
    P_dash_row2 = P_dash[1]
    P_dash_row3 = P_dash[2]

    P_row1 = P[0], 
    P_row2 = P[1], 
    P_row3 = P[2]
    for i in range(len(inlsrc_pts)):
        x,y = inlsrc_pts[i]
        x_dash, y_dash = inldst_pts[i]

        A_triang = np.zeros([4,4])
        A_triang[0] = x*P_row3 - P_row1
        A_triang[1] = y*P_row3 - P_row2
        A_triang[2] = x_dash*P_dash_row3 - P_dash_row1
        A_triang[3] = y_dash*P_dash_row3 - P_dash_row2
        
        U_triang, S_triang, V_triang = np.linalg.svd(A_triang)
        X_real_world = V_triang[-1]
        X_real_world = X_real_world/ (X_real_world[3])
        World_points.append(X_real_world)

    return World_points
