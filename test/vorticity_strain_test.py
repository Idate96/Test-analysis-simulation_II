import unittest
import numpy as np


def build_test_vectors(a, b, c):
    x = np.linspace(0, 1, a)
    y = np.linspace(0, 2, b)
    z = np.linspace(0, 3, c)
    pos = np.zeros((a, b, c, 3))
    vel = np.zeros((a, b, c, 3))
    for i in range(len(x)):
        for j in range(len(y)):
            vel[i, j, k] = linear_vector_field(x[i], y[j], z[k])
    return vel


def linear_vector_field(x, y, z):
    velocity = 10 * np.array((x, y, z))
    return velocity


def gradient(dim, array):
    pass


class Test_vorticity(unittest.TestCase):

    def test(self):
        pass


if __name__ == '__main__':

    vel = build_test_vectors(2, 2, 2)
    print(vel[:, 0, 0])

    x = np.linspace(0, 1, 3)
    y = np.linspace(0, 2, 3)
    z = np.linspace(0, 3, 3)
