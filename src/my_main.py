import numpy as np
from load_file import *
import vortex_detection
import vorticity_strain
from drag import *


def drag_calculation(exp):
    U = int(exp)
    x, y, vel = load_data("Velocity_" + exp, zeros=True)
    # conversion to meters
    xx, yy = np.meshgrid(x, y)

    u_grad, v_grad, w_grad = vorticity_strain.velocity_gradients(vel)
    u_grad, v_grad, w_grad = np.asarray(u_grad), np.asarray(v_grad), np.asarray(w_grad)

    x, y, std = load_data("StD_vel" + exp, zeros=True)
    x, y = x / 100, y / 100
    var_xx = std[0, :, :] ** 2
    var_yy = std[1, :, :] ** 2
    re_stress = np.zeros((2, 2, *np.shape(var_xx)))
    re_stress[0, 0] = var_xx
    re_stress[1, 1] = var_yy
    re_stress_stream = std[2, :, :] ** 2
    # with units
    re_stress_stream *= U ** 2

    pressure = pressure_term(vel[0], vel[1], u_grad, v_grad, (x, y), re_stress, U)
    print(np.max(vel[2, :, :]))
    conv_drag = convective_drag(vel[2, :, :], U, (x, y[:-1]))
    pr_drag = pressure_drag(pressure, 0, (x, y[11:]))
    re_drag = -fluctuation_drag(re_stress_stream, (x, y[:-1]))

    print("Convective drag: {0:.4f} \nPressure drag : {1:.4f} \nRe stress drag : {2:.4f}"
          .format(conv_drag, pr_drag, re_drag))
    drag = conv_drag + pr_drag + re_drag
    print("Total drag: ", drag)

def parse_shit_out(domain_bottom, domain_top):
    pass

if __name__ == '__main__':



    U = 4
    x, y, vel = load_data("Velocity_04", zeros=True)
    # conversion to meters
    x, y = x[7:], y[7:]
    xx, yy = np.meshgrid(x, y)

    u_grad, v_grad, w_grad = vorticity_strain.velocity_gradients(vel)
    u_grad, v_grad, w_grad = np.asarray(u_grad), np.asarray(v_grad), np.asarray(w_grad)

    x, y, std = load_data("StD_vel04", zeros=True)
    x, y = x[6:], y[6:]
    x, y = x / 100, y / 100
    var_xx = std[0, :, :] ** 2
    var_yy = std[1, :, :] ** 2
    re_stress = np.zeros((2, 2, *np.shape(var_xx)))
    re_stress[0, 0] = var_xx
    re_stress[1, 1] = var_yy
    re_stress_stream = std[2, :, :] ** 2 * U ** 2

    pressure = pressure_term(vel[0], vel[1], u_grad, v_grad, (x, y), re_stress, U)
    conv_drag = convective_drag(vel[2, :, :], U, (x, y[:-1]))
    pr_drag = pressure_drag(pressure, 0, (x, y[:-1]))
    re_drag = -fluctuation_drag(re_stress_stream, (x, y[:-1]))

    print("Convective drag: {0:.3f} \nPressure drag : {1:.3f} \nRe stress drag : {2:.3f}"
          .format(conv_drag, pr_drag, re_drag))
    drag = conv_drag + pr_drag + re_drag
    print("Total drag: ", drag)
    print(np.max(pressure))
    drag_calculation("04")
    countour_data_plot(xx, yy, pressure[7:, 7:])
    # print(np.type(u_hess2))
    # print(np.max(u_hess2[1] - u_hess[0]))

    # conv_drag = convective_drag(vel[2, :, :], U, (x, y[:-1]))
    # print(conv_drag)
    #
    x_b, y_b, stress_zz_b = load_stress("Re_bottom_04/B00005.dat")
    x_b, y_b, stress_zz_b = x_b / 10, y_b / 10, stress_zz_b / U ** 2
    xx_b, yy_b = np.meshgrid(x_b, y_b)
    countour_data_plot(xx_b, yy_b, stress_zz_b, "Re stress_zz bottom", r"$w'^2$", save=True) #

    x_t, y_t, stress_zz_t = load_stress("Re_top_04/B00005.dat")
    x_t, y_t, stress_zz_t = x_t / 10, y_t / 10, stress_zz_t / U ** 2

    xx_t, yy_t = np.meshgrid(x_t, y_t)
    # countour_data_plot(xx_t, yy_t, stress_zz_t, "Re stress_zz top", r"$w'^2$", save=True)

    x = x_b[11:-12]
    # y_t += y_b[-1]
    print('shape y-t {0}' .format(np.shape(y_t)))
    print('shape y-b {0}' .format(np.shape(y_b)))
    y = np.hstack((y_b, y_t))
    stress_zz_b = stress_zz_b[:,11:-12]
    print("shape stress bottom {0} \nShape stress top {1}" .format(np.shape(stress_zz_b), np.shape(stress_zz_t)))
    stress = np.vstack((stress_zz_t, stress_zz_b))
    xx,yy = np.meshgrid(x,y)
    print("y top ", y_t)
    print("y bottom", y_b)
    # countour_data_plot(xx, yy, stress, "total stress")
    #
    x, y, std = load_data("StD_vel04")
    print("shape y tot ", np.shape(y))
    print("y tot ", y)
    # var_zz = std[2, :, :] ** 2
    # xx, yy = np.meshgrid(x, y)
    # countour_data_plot(xx, yy, var_zz, "Re stress_zz total", r"$w'^2$", save=True)
