import numpy as np
from load_file import *
import vortex_detection
import vorticity_strain
from drag import *

if __name__ == '__main__':
    U = 4
    x, y, vel = load_data("Velocity_04", zeros=True)
    # conversion to meters
    x, y = x / 100, y / 100
    xx, yy = np.meshgrid(x, y)

    u_grad, v_grad, w_grad = vorticity_strain.velocity_gradients(vel)
    u_grad, v_grad, w_grad = np.asarray(u_grad), np.asarray(v_grad), np.asarray(w_grad)

    x, y, std = load_data("StD_vel04", zeros=True)
    var_xx = std[0, :, :] ** 2
    var_yy = std[1, :, :] ** 2
    re_stress = np.zeros((2, 2, *np.shape(var_xx)))
    re_stress[0, 0] = var_xx
    re_stress[1, 1] = var_yy

    pressure = pressure_term(vel[0], vel[1], u_grad, v_grad, (x, y), re_stress)
    countour_data_plot(xx, yy, pressure)

    # print(np.type(u_hess2))
    # print(np.max(u_hess2[1] - u_hess[0]))

    # conv_drag = convective_drag(vel[2, :, :], U, (x, y[:-1]))
    # print(conv_drag)
    #
    # x_b, y_b, stress_zz_b = load_stress("Re_bottom_04/B00005.dat")
    # x_b, y_b, stress_zz_b = x_b / 10, y_b / 10, stress_zz_b / U ** 2
    # xx_b, yy_b = np.meshgrid(x_b, y_b)
    # countour_data_plot(xx_b, yy_b, stress_zz_b, "Re stress_zz bottom", r"$w'^2$", save=False)
    #
    # x_t, y_t, stress_zz_t = load_stress("Re_top_04/B00005.dat")
    # x_t, y_t, stress_zz_t = x_t / 10, y_t / 10, stress_zz_t / U ** 2
    # xx_t, yy_t = np.meshgrid(x_t, y_t)
    # countour_data_plot(xx_t, yy_t, stress_zz_t, "Re stress_zz top", r"$w'^2$", save=False)
    #
    # x, y, std = load_data("StD_vel04")
    # var_zz = std[2, :, :] ** 2
    # xx, yy = np.meshgrid(x, y)
    # countour_data_plot(xx, yy, var_zz, "Re stress_zz total", r"$w'^2$", save=True)
