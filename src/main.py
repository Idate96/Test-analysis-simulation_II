import numpy as np
from load_file import *
import vortex_detection
import vorticity_strain


if __name__ == '__main__':
    # scaling parameter for vortcity
    L = 0.5
    # load position and velocity
    exp = 'Velocity_16'
    x, y, vel = load_data(exp)
    xx, yy = np.meshgrid(x, y)

    # quiver plot

    # quiver_data_plot(xx, yy, vel[2, :, :], vel[:2, :, :],
    #  'Normalized z velocity', 'w/U', save=False)

    # 3d plotting
    # plot_data_3d(xx, yy, vel[0, :, :])
    # plot_data_3d(xx, yy, vel[1, :, :])
    # plot_data_3d(xx, yy, vel[2, :, :])
    #
    # # countour plotting
    countour_data_plot(xx, yy, vel[0, :, :], 'Normalized x velocity', 'u/U', save=False)
    countour_data_plot(xx, yy, vel[1, :, :], 'Normalized y velocity', 'v/U', save=False)
    countour_data_plot(xx, yy, vel[2, :, :], 'Normalized z velocity', 'w/U', save=False)

    # quiver_data_plot(xx, yy, vel[2, :, :], vel[:2, :, :],
    #                  'Normalized z velocity', 'w/U', save=False)

    # quiver_data_plot(xx, yy, vel[2, :, :], vel[:2, :, :],
    #'Normalized z velocity', 'w/U', save=True)

    # vortex detection preliminaries
    u_grad, v_grad, w_grad = vorticity_strain.velocity_gradients(vel)
    u_grad, v_grad, w_grad = np.asarray(u_grad), np.asarray(v_grad), np.asarray(w_grad)
    quiver_data_plot(xx, yy, vel[0, :, :], u_grad,
                     'u', 'u/U', save=False)
    vorticity_value = vorticity_strain.find_vorticity(u_grad, v_grad)
    strain = vorticity_strain.find_strain(u_grad, v_grad)
    vort_tens = vorticity_strain.construct_vorticity_tensor(u_grad, v_grad)
    strain_tensor = vorticity_strain.contruct_strain_tensor(u_grad, v_grad)

    # Quiver with vorticity overlap
    quiver_data_plot(xx, yy, vorticity_value, vel[:2, :, :], 'Vorticity', 'w/U', save=False)

    # plot strain and vorticity
    countour_data_plot(xx, yy, strain, 'Strain', r'S', save=False)
    countour_data_plot(xx, yy, vorticity_value, 'Vorticity', 'Omega [1\s]', save=False)
    vortexcenter_scatter_plot(xx, yy, vorticity_value, vortex_detection.discrete_method(
        vel), 'Vorticity', 'Omega [1\s]', save=False)
    quiver_data_plot(xx, yy, vel[2, :, :], vel[:2, :, :],
                     'Normalized z velocity', 'w/U', vortex_centers=vortex_detection.discrete_method(vel),
                     save=True, show=False)

    # Add mannequin: put show=False in plot you want to see the mannequin in
    AddMannequin()

    quiver_data_plot(xx, yy, vorticity_value, vel[:2, :, :],
                     'Vorticity', 'Omega [1\s]', vortex_centers=vortex_detection.discrete_method(vel),
                     save=True, show=False)

    # Add mannequin: put show=False in plot you want to see the mannequin in
    AddMannequin()

    # vortex detection
    q = vortex_detection.q_test(vort_tens, strain_tensor)
    mask = np.where(q > 0)
    q[mask] *= 10

    #countour_data_plot(xx, yy, q, 'Q test vortex detection', 'Q', save=False)

    countour_data_plot(xx, yy, q, 'Q test vortex detection', 'Q', save=True, show=False)

    AddMannequin()

    delta = vortex_detection.delta_test(u_grad, v_grad)
    mask = np.where(delta > 0)
    delta[mask] *= 10

    #countour_data_plot(xx, yy, delta, 'Delta vortex detection', 'Delta', save=False)

    countour_data_plot(xx, yy, delta, 'Delta vortex detection', 'Delta', save=True, show=False)

    AddMannequin()
