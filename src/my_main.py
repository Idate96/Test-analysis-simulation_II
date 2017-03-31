import numpy as np
from load_file import *
import vortex_detection
import vorticity_strain
from drag import convective_drag

if __name__ == '__main__':
    U = 4
    # exp = '04'
    # x, y, vel = load_data(exp, zeros=True)
    # # conversion to meters
    # x, y = x / 100, y / 100
    # xx, yy = np.meshgrid(x, y)
    #
    # conv_drag = convective_drag(vel[2, :, :], U, (x, y[:-1]))
    # print(conv_drag)

    x_b, y_b, stress_zz_b = load_stress("Re_bottom_04/B00006.dat")
    x_b, y_b, stress_zz_b = x_b / 10, y_b / 10, stress_zz_b / U ** 2
    xx_b, yy_b = np.meshgrid(x_b, y_b)
    countour_data_plot(xx_b, yy_b, stress_zz_b, "Re stress_zz bottom", r"$w'^2$", save=True)
    x_t, y_t, stress_zz_t = load_stress("Re_top_04/B00006.dat")
    x_t, y_t, stress_zz_t = x_t / 10, y_t / 10, stress_zz_t / U ** 2
    xx_t, yy_t = np.meshgrid(x_t, y_t)
    countour_data_plot(xx_t, yy_t, stress_zz_t, "Re stress_zz top", r"$w'^2$", save=True)

    x, y, std = load_data("StD_vel04")
    var_zz = std[2, :, :] ** 2
    xx, yy = np.meshgrid(x, y)
    countour_data_plot(xx, yy, var_zz, "Re stress_zz total", r"$w'^2$", save=True)
