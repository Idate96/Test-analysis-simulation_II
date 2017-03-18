import numpy as np
import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import pdb


def central_diff_1o2(func_pts, x):
    df = np.zeros((np.size(x)))
    for i in range(1, len(x) - 1):
        df[i] = (func_pts[i + 1] - func_pts[i - 1]) / (x[i + 1] - x[i - 1])
    return df


def parse_structured_grid(data):
    # init dimesion fo array
    rows = 0
    columns = 0
    # set initial value arra
    initial_value_x = data[0, 0]
    # find # dof in y and x dimension of data set
    for i, element in enumerate(data[:, 0]):
        if element == initial_value_x:
            if columns == 0:
                columns = i - columns
            rows += 1
    # fist row is missing replace it with fictional value
    fict_value = np.array((data[columns - 1, 0], data[0, 1]))
    data = np.vstack((fict_value, data))
    # assumed structured grid
    x = data[:columns, 0]
    y = data[::columns, 1]
    return x, y, (rows, columns)


def load_data(experiment='16'):
    data = np.loadtxt(dir_path + "/../exp_data/Velocity_" + experiment + ".plt", skiprows=4)
    position = data[:, :2]
    x, y, dim = parse_structured_grid(position)
    # data is missing one row
    first_row = np.array((0))
    # stack missing row and reshape according to the dimensions of the grid
    u = np.hstack((first_row, data[:, 3])).reshape(dim)
    v = np.hstack((first_row, data[:, 4])).reshape(dim)
    vel = np.array((u, v))
    return x, y, vel


if __name__ == '__main__':
    load_data()
