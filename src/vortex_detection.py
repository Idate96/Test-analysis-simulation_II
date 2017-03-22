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


<<<<<<< HEAD
=======
def lambda_test(vorticity_tens, strain_tens):
    """This does not work in 2d."""
    vort_tens_sq = np.empty(np.shape(vorticity_tens))
    strain_tens_sq = np.empty(np.shape(strain_tens))
    for i in range(np.shape(vorticity_tens)[0]):
        for j in range(np.shape(vorticity_tens)[1]):
            vort_tens_sq[i, j] = np.square(vort_tens[i, j])
            strain_tens_sq[i, j] = np.square(strain_tens[i, j])
    M = vort_tens_sq + strain_tens

    eigenvalues = np.empty((*np.shape(M[0, 0]), 2))
    for i in range(np.shape(M[0, 0])[0]):
        for j in range(np.shape(M[0, 0])[1]):
            if np.isnan(M[:, :, i, j]).any():
                M[:, :, i, j] = np.nan_to_num(M[:, :, i, j])
            eigenvalues[i, j], eig_vect = np.linalg.eig(M[:, :, i, j])
            eigenvalues[i, j] = np.sort(eigenvalues[i, j])

    return eigenvalues[:, :, 0]


>>>>>>> 190fb8a45ee6a716c9371508aae04f7507d91465
def discrete_method(velocity):
    """This module uses a discrete method to determine vortex centers.

    First it evaluates at every point if the condition for a vortex center

    holds. Then it lets these vortices grow until no new points that satisfy

    the condition are found.

    Arg:

        velcity (np array)  = velocity array as defined by load_data function.

    Returns:

        List of coordinates at which a vortex center is present accourding to

        the discrete method.
    """


    # The position  indices of the vortex centers will be stored in a list.
    vortex_center_indices = []

    u_vel = velocity[0]
    v_vel = velocity[1]
    w_vel = velocity[2]
    rows, columns = np.shape(u_vel)

    for i in range(1, rows-1):
        for j in range(1, columns-1):

            check1 = np.sign(u_vel[i-1, j]) + np.sign(u_vel[i+1, j]) + np.sign(v_vel[i, j+1]) + np.sign(v_vel[i, j-1])
            check2 = np.sign(u_vel[i-1, j]) + np.sign(v_vel[i, j+1])

            if (check1 == 0.) and (check2 != 0.):
                strength = abs(u_vel[i-1, j]) + abs(u_vel[i+1, j]) + abs(v_vel[i, j+1]) + abs(v_vel[i, j-1])
                vortex_center_indices.append((i, j, strength))
    return vortex_center_indices

if __name__ == '__main__':
    pass
