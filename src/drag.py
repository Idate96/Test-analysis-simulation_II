"""In this module there are methods to calculated drag from discrete vector field data."""
import numpy as np
import vorticity_strain
from load_file import *


def simpson_quad_2d(func, domain):
    """Simpson quadrature 2d. Error O(h^3) exact for p ∈ P_3."""
    assert np.size(domain[0]) % 2 != 0 and np.size(
        domain[1]) % 2 != 0, "Simpson rule not applicable dim % 2 == 0"

    dim = (len(domain[0]), len(domain[1]))
    x, y = domain
    elem_integral = np.zeros((int((dim[0] - 1) / 2), int((dim[1] - 1) / 2)))

    for i in range(0, dim[1] - 1, 2):
        for j in range(0, dim[0] - 1, 2):
            J = (x[j + 2] - x[j]) * (y[i + 2] - y[i]) / 4
            elem_integral[int(j / 2), int(i / 2)] = J / 9 * (
                func[i, j] + func[i, j + 2] + func[i + 2, j] + func[i + 2, j + 2] +
                4 * (func[i, j + 1] + func[i + 1, j] + func[i + 1, j + 2] + func[i + 2, j + 1]) +
                16 * (func[i + 1, j + 1]))

    return np.sum(elem_integral)


def convective_drag(w, U, domain):
    rho = 1.225
    integrand = w * (1 - w)
    drag_conv = rho * U ** 2 * simpson_quad_2d(integrand, domain)
    return drag_conv


def forward_euler(f, u, dt):
    """Explicit forward euler scheme."""
    if callable(f):
        u = u + dt * (f(u))
    elif isinstance(f, (float, np.ndarray)):
        u = u + dt * (f)
    return u


def quad_simpson(f_values, x, exact_int=0):
    """Simpson quadrature.

        Args:
            a (float) = integration interval start
            b (float) = integration interval end
            n (int) = number of subintervals of integration
            f (obj func) = function to be integrated.
            exact_int (float : optional) = exact integral value

        Returns:
            integral_value (float) = value of the integral_value.
            error (float) = error of integration if available
    """
    # x = np.linspace(a, b, n + 1)
    # h = (b - a) / n
    # num_int = h / 2 * (1 / 3 * f(x) + 4 / 3 * f(x + h / 2) + 1 / 3 * f(x + h))
    # integral_value = np.sum(num_int[:-1])
    integral = np.zeros((np.size(x) - 2))
    for i in range(1, np.size(x) - 2):
        integral[i] = (x[i + 1] - x[i]) / 2 * (1 / 3 * f_values[i - 1] +
                                               4 / 3 * f_values[i] + 1 / 3 * f_values[i + 1])
        # integral[i] = (x[i+1] - x[i])/2 * (f_values[i] + f_values[i+1])
    return np.sum(integral)


def plot_drag_cilinder(list_exp):

    rho = 1.225
    D = 0.07
    din_visc = 18.46 * 10 ** (-6)
    cds = []
    Res = []

    for exp in list_exp:
        x, y, vel = load_cylinder_data(exp)
        U = int(exp) / 100
        u_norm = vel[0, :, 5] / U
        drag = drag_cilinder(u_norm, U, y)
        cd = drag / (0.5 * rho * U**2 * D)
        Re = rho * U * D / din_visc
        Res.append(Re)
        cds.append(cd)
    plt.scatter(Res, cds)
    plt.show()
    return Res, cds


def drag_cilinder(w, U, domain):
    rho = 1.225
    integrand = w * (1 - w)
    drag_conv = rho * U ** 2 * quad_simpson(integrand, domain)
    return drag_conv / 1000


def adam_bashfort(f, u, u_0, dt):
    """Adam bashfort 2 step method.

    Args:
        f (obj func) = function coming from the ODE u' = f(u)
        u (np.ndarray) = state vector at t_i
        u_0 (np.ndarray) = state vector at t_i-1
        dt (float) = time step

    Returns:
        u (np.ndarray) = state vector at t_i+1
    """
    if callable(f):
        u = u + dt * (3 / 2 * f(u) - f(u_0))
    elif isinstance(f, (float, np.ndarray)):
        u = u + dt * (3 / 2 * f * u - f * u_0)
    return u


def test_func(x, y):
    return 1 - 2 * x ** 4 - y ** 2


def pressure_term(u, v, u_grad, v_grad, domain, re_stress, U):

    pressure = np.zeros(np.shape(u))
    pressure[:, 0] = 0
    u_hess = vorticity_strain.hessian(u)
    # v_hess = vorticity_strain.hessian(v)
    grad_re_stress_00 = np.asarray(np.gradient(re_stress[0, 0])) * U
    grad_re_stress_01 = np.asarray(np.gradient(re_stress[0, 1])) * U
    u = U * u
    v = U * v
    rho = 1.225
    mu = 18.46 * 10 ** (-6)
    x, y = domain
    dx = x[1] - x[0]  # constant spacing

    # now integrating from right domiain range(,,-1) and -dx in the integrator
    for i in range(np.size(y) - 10, 5, -1):
        for j in range(np.size(x) - 10, 5, -1):
            rhs_1 = -rho * (u[i, j] * u_grad[1, i, j] +
                            v[i, j] * v_grad[0, i, j])
            rhs_2 = -rho * \
                (grad_re_stress_00[1, i, j] + grad_re_stress_01[0, i, j])
            rhs_3 = mu * (u_hess[0, 0, i, j] + u_hess[1, 1, i, j])
            rhs = rhs_1 + rhs_2 + rhs_3
            pressure[i, j - 1] = forward_euler(rhs, pressure[i, j], -dx)
            # pressure[i+1,j+1] = 1
    # the pressure term has units of Pa * s/ m (since gradient and velocity
    # dimensionless)
    x = x[5:-10]
    y = y[5:-10]
    xx, yy = np.meshgrid(x, y)
    plt.plot(xx, yy, pressure)
    return pressure


def pressure_drag(pressure, pressure_inf, domain):
    integrand = pressure_inf - pressure
    drag_pressure = simpson_quad_2d(integrand, domain)
    return drag_pressure


def fluctuation_drag(std_streamwise, domain):
    rho = 1.225
    drag = rho * simpson_quad_2d(std_streamwise, domain)
    return drag


if __name__ == '__main__':
    # x, y, vel = load_cylinder_data("0903")
    # print(np.shape(x), np.shape(vel[0].reshape(344, np.size(vel[0])/344)))
    # print(np.shape(y))
    print(np.shape(vel[0]))
    xx, yy = np.meshgrid(x, y)
    countour_data_plot(xx, yy, vel[0], color=cm.coolwarm)
    # drag = drag_cilinder(vel[0,:,0]/9.07,9.07, y)
    # print("Drag ", drag)
    # print("Cd ", drag/(0.5*1.225*9.07**2*0.07))

    # res, cds  = plot_drag_cilinder(['0903', '1278','1807','1895','2556'])
    # print("res {0}\ncds {1}" .format(res, cds))
    # print(vel[0])
    # x, y = np.linspace(-2, 2, 31), np.linspace(0, 1, 51)
    # xx, yy = np.meshgrid(x, y)
    # func = test_func(xx, yy)
    # integral = simpson_quad_2d(func, (x, y))
    # print("Value integral : ", integral)
    pass
