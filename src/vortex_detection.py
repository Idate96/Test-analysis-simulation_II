"""This module contains different condition algorithms.

to detect vortices in the velocity field.
"""

import numpy as np

def discrete_method(velgrid):
    """This module uses a discrete method to determine vortex centers.

    First it evaluates at every point if the condition for a vortex center

    holds. Then it lets these vortices grow until no new points that satisfy

    the condition are found.

    Arg:

        pos_pt (Tuple) = storage number of a point in the grid , ie (1,0).
        velgrid (np array) = velocity components in the grid.
    """

    #The indices of the vortex centers will be stored in a list.

    vortex_center_ind = []
    for i, row in enumerate(velgrid):
        for j, element in enumerate(velgrid):
            vel0 = velgrid[i,j]     #velocity of the actual point
            vel1 = velgrid[i-1,j]   #velocity of the left point
            vel2 = velgrid[i,j+1]   #velocity of the top point
            vel3 = velgrid[i+1,j]   #velocity of the right point
            vel4 = velgrid[i,j-1]   #velocity of the bottom point

            check1 = np.sign(vel1[0])+np.sign(vel3[0])+np.sign(vel2[1])+np.sign(vel4[1])
            check2 = np.sign(vel1[0])+np.sign(vel2[1])
            check3 =

            if (int(check1) == 0) and (int(check2) != 0) and not (np.all(vel1) == 0):
                vortex_center_ind.append((i,j))
