"""In this module there are methods to calculated drag from discrete vector field data."""
import numpy as np


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


def test_func(x, y):
    return 1 - 2 * x ** 4 - y ** 2

if __name__ == '__main__':
    x, y = np.linspace(-2, 2, 31), np.linspace(0, 1, 51)
    xx, yy = np.meshgrid(x, y)
    func = test_func(xx, yy)
    integral = simpson_quad_2d(func, (x, y))
    print("Value integral : ", integral)
