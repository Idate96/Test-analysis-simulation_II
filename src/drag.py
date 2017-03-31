"""In this module there are methods to calculated drag from discrete vector field data."""
import numpy as np
import vorticity_strain


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


def pressure_term(u, v, u_grad, v_grad, domain, re_stress):

    pressure = np.zeros(np.shape(u))
    pressure[:, 0] = 0
    u_hess = vorticity_strain.hessian(u)
    # v_hess = vorticity_strain.hessian(v)
    grad_re_stress_00 = np.asarray(np.gradient(re_stress[0, 0]))
    grad_re_stress_01 = np.asarray(np.gradient(re_stress[0, 1]))
    rho = 1.225
    mu = 18.27 * 10 ** (-6)
    x, y = domain
    dx = x[1] - x[0]  # constant spacing

    for i in range(np.size(y) - 2, 0, -1):
        for j in range(np.size(x) - 2, 0, -1):
            rhs_1 = -rho * (u[i, j] * u_grad[1, i, j] + v[i, j] * v_grad[0, i, j])
            rhs_2 = -rho * (grad_re_stress_00[1, i, j] + grad_re_stress_01[0, i, j])
            rhs_3 = mu * (u_hess[0, 0, i, j] + u_hess[1, 1, i, j])
            rhs = rhs_1 + rhs_2 + rhs_3
            print(rhs)
            pressure[i, j - 1] = forward_euler(rhs, pressure[i, j], -dx)
            # pressure[i+1,j+1] = 1
    return pressure


if __name__ == '__main__':
    # x, y = np.linspace(-2, 2, 31), np.linspace(0, 1, 51)
    # xx, yy = np.meshgrid(x, y)
    # func = test_func(xx, yy)
    # integral = simpson_quad_2d(func, (x, y))
    # print("Value integral : ", integral)
    pass
