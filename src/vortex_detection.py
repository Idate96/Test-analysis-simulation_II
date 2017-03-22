"""This module contains different condition algorithms to detect vortices in the velocity field.
"""
import numpy as np
import vorticity_strain
import pdb


def q_test(vorticity_t, strain_t):
    Q = np.empty(np.shape(strain_t)[2:])
    # pdb.set_trace()
    for i in range(np.shape(strain_t)[2]):
        for j in range(np.shape(strain_t)[3]):
            vorticity_norm = np.linalg.norm(vorticity_t[:, :, i, j], 'fro')
            strain_norm = np.linalg.norm(strain_t[:, :, i, j], 'fro')
            Q[i, j] = 0.5 * (vorticity_norm - strain_norm)
    return Q


def delta_test(u_grad, v_grad):

    vorticity_t = vorticity_strain.construct_vorticity_tensor(u_grad, v_grad)
    strain_t = vorticity_strain.contruct_strain_tensor(u_grad, v_grad)
    jacobian = vorticity_strain.jacobian_matrix(u_grad, v_grad)

    q = q_test(vorticity_t, strain_t)

    delta = np.empty(np.shape(strain_t)[2:])

    for i in range(np.shape(strain_t)[2]):
        print(i)
        for j in range(np.shape(strain_t)[3]):
            delta[i, j] = ((q[i, j] / 3) ** 3 + (np.linalg.det(jacobian[:, :, i, j]) / 2) ** 2)
    return delta


def discrete_method(velocity):
    """This module uses a discrete method to determine vortex centers.

    First it evaluates at every point if the condition for a vortex center

    holds. Then it lets these vortices grow until no new points that satisfy

    the condition are found.

    Arg:

        pos_pt (Tuple) = storage number of a point in the grid , ie (1,0).
        velocity (np array) = velocity components in the grid.
    """


    # The position  indices of the vortex centers will be stored in a list.
    vortex_center_indices = []
    u_vel = velocity[0]
    v_vel = velocity[1]
    w_vel = velocity[2]
    rows, columns = np.shape(u_vel)

    for i in range(1, rows-1):
        for j in range(1, columns-1):
            print(i)
            print(j)


            # vel0 = velocity[j, k]  # velocity of the actual point
            # vel1 = velocity[i - 1, j]  # velocity of the left point
            # vel2 = velocity[i, j + 1]  # velocity of the top point
            # vel3 = velocity[i + 1, j]  # velocity of the right point
            # vel4 = velocity[i, j - 1]  # velocity of the bottom point
            check1 = np.sign(u_vel[i-1, j]) + np.sign(u_vel[i+1, j]) + np.sign(v_vel[i, j+1]) + np.sign(v_vel[i, j-1])
            check2 = np.sign(u_vel[i-1, j]) + np.sign(v_vel[i, j+1])
            print(check1)
            if (check1 == 0.) and (check2 != 0.):
                vortex_center_indices.append((i, j))

    return vortex_center_indices

if __name__ == '__main__':
    pass
