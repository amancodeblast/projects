from TriangulationLinear import TriangulationLinear
import numpy as np
def DisambiguateCameraPose(inlsrc_pts, inldst_pts, P, P_dash, K, R, C):
    '''
    inlsrc_pts: List of 463,2
    inldst_pts: List of 463,2
    P: (3,4)
    P_dash: (4, 3, 4)
    K: (3,3) len list
    R: 4 length list (3,3)

    C:  4,3 length list 
    '''
    I = np.identity(3)
    max_positive_count = 0
    final_m = 5
    for m in range(4): # number of possibilities
        count = 0
        World_points = TriangulationLinear(inlsrc_pts, inldst_pts, P, P_dash[m], K) # list of 463, 4
        Cam_center2 = -np.dot(I,np.dot(np.linalg.inv(R[m]),C[m])) # -I@(inv_R@C) but done using np.dot because its list 

        Cam_center1 = [0,0,0]
        R1_2 = [0,0,1] # for z axis measure to be positive
        for i in range(len(World_points)):
            cheirality1 = np.dot(R1_2,(World_points[i][0:3]-Cam_center1))  # for z positive
            cheirality2 = np.dot(np.transpose(R[m][:,2]),(World_points[i][0:3]-Cam_center2))
#original code            #cheirality2 = np.dot(np.transpose(R[m][2]),(World_points[i][0:3]-Cam_center2))
            if cheirality2>0 and cheirality1>0:
                count += 1
        print('number of positive Z values', count)
        if count > max_positive_count:
            max_positive_count = count
            final_m = m
#        X_proj_dst = np.dot(np.dot(K,P_dash[m]), World_points[4])
#        X_proj_src = np.dot(np.dot(K,P), World_points[4])
    
    pose_index = final_m
    # could save the next step by storing the world points for the best one 
    World_points_for_correct_pose = TriangulationLinear(inlsrc_pts, inldst_pts, P, P_dash[final_m], K)
    
    return World_points_for_correct_pose, pose_index