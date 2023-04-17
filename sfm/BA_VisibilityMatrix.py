import numpy as np
def AdaptiveVisibility(n, Vis_available, World_points, list_len_new, common_worldpoints):
    '''
    Input:
    n : 3
    Vis_available: (2, 463)
    list_len_new: 47
    len of World_points : 510
    len of common_worldpoints: 90

    Output: 
    new_visibility_mat : (3, 506)
    '''
    list_len1 = Vis_available.shape[1]#(2, 463)
    new_column = np.zeros([len(World_points),1]) # 506,1 
    new_column[list_len1: list_len1+list_len_new] = 1

    for i in range(len(World_points)):
        for j in range(len(common_worldpoints)):
            if (World_points[i][0] == common_worldpoints[j][0] and World_points[i][1] == common_worldpoints[j][1]):
                new_column[i]= 1

    new_visibility_mat = np.zeros([n,len(World_points)])# (3, 506)
    new_visibility_mat[n-1] = np.ravel(new_column) # new_visibility_mat: (3, 506), new_column: (506, 1)
    old_rows, old_columns = Vis_available.shape # (2, 463)
    new_visibility_mat[0:old_rows, 0:old_columns] = Vis_available
    new_visibility_mat[0] = 1

    return new_visibility_mat