import numpy as np
from load_file import *
import vortex_detection
import vorticity_strain

if __name__ == '__main__':
    # load position and velocity
    exp = '04'
    x, y, vel = load_data(exp)
    xx, yy = np.meshgrid(x, y)

    # 3d plotting
    plot_data_3d(xx, yy, vel[0, :, :])
    plot_data_3d(xx, yy, vel[1, :, :])
    plot_data_3d(xx, yy, vel[2, :, :])

    # countour plotting
    countour_data_plot(xx, yy, vel[0, :, :], 'Normalized x velocity', 'u/U', save=True)
    countour_data_plot(xx, yy, vel[1, :, :], 'Normalized y velocity', 'v/U', save=True)
    countour_data_plot(xx, yy, vel[2, :, :], 'Normalized z velocity', 'w/U', save=True)

    # vortex detection preliminaries
    u_grad, v_grad, w_grad = vorticity_strain.velocity_gradients(vel)
    vorticity_value = vorticity_strain.find_vorticity(u_grad, v_grad)
    strain = vorticity_strain.find_strain(u_grad, v_grad)
    vort_tens = vorticity_strain.construct_vorticity_tensor(u_grad, v_grad)
    strain_tensor = vorticity_strain.contruct_strain_tensor(u_grad, v_grad)

    # plot strain and vorticity
    countour_data_plot(xx, yy, strain, 'Strain', r'S', save=True)
    countour_data_plot(xx, yy, vorticity_value, 'Vorticity', 'Omega [1\s]', save=True)

    # vortex detection methods
    q = vortex_detection.q_test(vort_tens, strain_tensor)
    countour_data_plot(xx, yy, q, 'Q test vortex detection', 'Q', save=True)

    delta = vortex_detection.delta_test(u_grad, v_grad)
    countour_data_plot(xx, yy, delta, 'Delta vortex detection', 'Delta', save=True)
