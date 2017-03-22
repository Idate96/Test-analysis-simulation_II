"""This module contains different condition algorithms to detect vortices in the velocity field.
"""
import numpy as np
import vorticity_strain
import load_file
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
        for j in range(np.shape(strain_t)[3]):
            delta[i, j] = ((q[i, j] / 3) ** 3 + (np.linalg.det(jacobian[:, :, i, j]) / 2) ** 2)
    return delta


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


def discrete_method(velgrid):
    """This module uses a discrete method to determine vortex centers.

    First it evaluates at every point if the condition for a vortex center

    holds. Then it lets these vortices grow until no new points that satisfy

    the condition are found.

    Arg:

        pos_pt (Tuple) = storage number of a point in the grid , ie (1,0).
        velgrid (np array) = velocity components in the grid.
    """

    # The indices of the vortex centers will be stored in a list.

    vortex_center_ind = []
    for i, row in enumerate(velgrid):
        for j, element in enumerate(velgrid):
            vel0 = velgrid[i, j]  # velocity of the actual point
            vel1 = velgrid[i - 1, j]  # velocity of the left point
            vel2 = velgrid[i, j + 1]  # velocity of the top point
            vel3 = velgrid[i + 1, j]  # velocity of the right point
            vel4 = velgrid[i, j - 1]  # velocity of the bottom point

            check1 = np.sign(vel1[0]) + np.sign(vel3[0]) + np.sign(vel2[1]) + np.sign(vel4[1])
            check2 = np.sign(vel1[0]) + np.sign(vel2[1])
            check3 = 0

            if (int(check1) == 0) and (int(check2) != 0) and not (np.all(vel1) == 0):
                vortex_center_ind.append((i, j))


if __name__ == '__main__':
    exp = '04'
    x, y, vel = load_file.load_data(exp)
    xx, yy = np.meshgrid(x, y)

    u_grad, v_grad, w_grad = vorticity_strain.velocity_gradients(vel)
    vorticity_value = vorticity_strain.find_vorticity(u_grad, v_grad)
    strain = vorticity_strain.find_strain(u_grad, v_grad)
    vort_tens = vorticity_strain.construct_vorticity_tensor(u_grad, v_grad)
    strain_tensor = vorticity_strain.contruct_strain_tensor(u_grad, v_grad)
    eigenvalues_2 = lambda_test(vort_tens, strain_tensor)
    load_file.countour_data_plot(xx, yy, eigenvalues_2)
