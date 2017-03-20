import numpy as np
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import pdb
from load_file import *
import vortex_detection


def velocity_gradients(velocity):
    """Calculate velocity gradients."""
    u_grad = np.gradient(velocity[0, :, :])
    v_grad = np.gradient(velocity[1, :, :])
    w_grad = np.gradient(velocity[2, :, :])
    return u_grad, v_grad, w_grad


def jacobian_matrix(u_grad, v_grad):
    jacobian = np.empty((2, 2, *np.shape(u_grad[0])))
    jacobian[0, 0] = u_grad[0]
    jacobian[0, 1] = u_grad[1]
    jacobian[1, 0] = v_grad[0]
    jacobian[1, 1] = v_grad[1]
    return jacobian


def find_vorticity(u_grad, v_grad):
    """Calculate vorticity.

    Args:
        u_grad (np.array : shape(2, *(dim_grid)) = gradient of u in the x (0) and y direction (1), ie u_grad[0,i,j] returns dudx[i,j]
        v_grad (np.array : shape(2, *(dim_grid)) = gradient of v in the x (0) and y direction (1), ie v_grad[0,i,j] returns dvdx[i,j]

    Returns:
        vorticity_01 (np.array :shape(*(shape_grid))) = component of the vorticity tensor
    """
    vorticity_01 = 0.5 * (u_grad[1] - v_grad[0])
    return vorticity_01


def find_strain(u_grad, v_grad):
    """Calculate strain.

        Args:
            u_grad (np.array : shape(2, *(dim_grid)) = gradient of u in the x (0) and y direction (1), ie u_grad[0,i,j] returns dudx[i,j]
            v_grad (np.array : shape(2, *(dim_grid)) = gradient of v in the x (0) and y direction (1), ie v_grad[0,i,j] returns dvdx[i,j]

        Returns:
            strain tensor (np.array : shape(2,2,*dim_grid)) = strain tensor stored in a matrix
    """
    strain_01 = 0.5 * (u_grad[1] + v_grad[0])
    return strain_01


def construct_vorticity_tensor(u_grad, v_grad):
    """Construct the strain tensor.
    Args:
        u_grad (np.array : shape(2, *(dim_grid)) = gradient of u in the x (0) and y direction (1), ie u_grad[0,i,j] returns dudx[i,j]
        v_grad (np.array : shape(2, *(dim_grid)) = gradient of v in the x (0) and y direction (1), ie v_grad[0,i,j] returns dvdx[i,j]

    Returns:
        vorticity tensor (np.array : shape(2,2,*dim_grid)) = vorticity tensor stored in a matrix

    """
    vorticity = find_vorticity(u_grad, v_grad)
    vorticity_tensor = np.zeros((2, 2, *np.shape(vorticity)))
    vorticity_tensor[0, 1] = vorticity
    vorticity_tensor[1, 0] = -vorticity
    return vorticity_tensor


def contruct_strain_tensor(u_grad, v_grad):
    """Construct strain tensor.
        Args:
            u_grad (np.array : shape(2, *(dim_grid)) = gradient of u in the x (0) and y direction (1), ie u_grad[0,i,j] returns dudx[i,j]
            v_grad (np.array : shape(2, *(dim_grid)) = gradient of v in the x (0) and y direction (1), ie v_grad[0,i,j] returns dvdx[i,j]

        Returns:
            strain tensor (np.array : shape(2,2,*dim_grid)) = strain tensor stored in a matrix
    """
    strain = find_strain(u_grad, v_grad)
    strain_tensor = np.zeros((2, 2, *np.shape(strain)))
    strain_tensor[0, 0] = u_grad[0]
    strain_tensor[1, 1] = v_grad[1]
    strain_tensor[1, 0] = strain_tensor[0, 1] = strain
    return strain_tensor

if __name__ == '__main__':
    # x, y, vel = load_data('04')
    # xx, yy = np.meshgrid(x, y)
    # u_grad, v_grad, w_grad = velocity_gradients(vel)
    # vorticity_value = find_vorticity(u_grad, v_grad)
    # strain = find_strain(u_grad, v_grad)
    # vort_tens = construct_vorticity_tensor(u_grad, v_grad)
    # strain_tensor = contruct_strain_tensor(u_grad, v_grad)
    # print(strain_tensor[:, :, 0, 0])
    # print(vort_tens)

    # countour_data_plot(xx, yy, strain)
    # countour_data_plot(xx, yy, vorticity_value)
    # q = vortex_detection.q_test(vort_tens, strain_tensor)
    # countour_data_plot(xx, yy, q)

    # delta = vortex_detection.delta_test(u_grad, v_grad)
    # countour_data_plot(xx, yy, delta)
