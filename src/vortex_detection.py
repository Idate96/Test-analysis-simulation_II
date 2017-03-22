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


<<<<<<< HEAD
def discrete_method(velocity):
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


def discrete_method(velgrid):
>>>>>>> 2c830ec2053c8bfea6c1b8f2fa9f93456e1114d6
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
