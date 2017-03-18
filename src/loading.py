# loading of the experimental data
# importing modules
import numpy as np

# loading the data (StD_vel04)


def load(x, y, location):
    # for location fill in the corresponding value in brackets in exp_data_kopie
    # 0<=x<=64
    # 0<=x<=64
    if location == 1:
        location = 'exp_data_kopie\StD_vel04(1).plt'
    if location == 2:
        location = 'exp_data_kopie\StD_vel16(2).plt'
    if location == 3:
        location = 'exp_data_kopie\Velocity_04(3).plt'
    if location == 4:
        location = 'exp_data_kopie\Velocity_16(4).plt'
    data = np.loadtxt(location)
    numb_loc = y * 53 + x
    return data[numb_loc]


def parse_structured_grid(data):
    """Parse and reorganize a structured grid.

    Args:
        data (np.array : shape (#dof, 2)) = first column contain the x coordinate of the dof, second column the y coordinate

    Returns:
        x (np.array) = 1d array of coordinates of the dof
        y (np.array) = 1d array of the y coordinates of the dof
        dim (tuple) = dimension of the grid

    Remark:
        since the grid it is structured x,y array give complete information.
        Grid can be generate with meshgrid(x,y).
    """
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


def load_data(experiment):
    """Load the experimental data.

    Args:
        experiment (str) = experiment label indicating U_∞
    Returns:
        x (np.array) = 1d array of coordinates of the dof
        y (np.array) = 1d array of the y coordinates of the dof
        vel (np.array) = vel[0,i,j] is the u of the point_ij and v[1,i,j] is the v of point_ij

    """
    try:
        if experiment not in ['16', '04']:
            raise ValueError()
    except ValueError:
        print("Choose between '16' or '04'")
    data = np.loadtxt(dir_path + "/../exp_data/Velocity_" + experiment + ".plt", skiprows=4)
    # select columns data reppresenting position
    position = data[:, :2]
    x, y, dim = parse_structured_grid(position)
    # data is missing one row
    first_row = np.array((0))
    # stack missing row and reshape according to the dimensions of the grid
    u = np.hstack((first_row, data[:, 3])).reshape(dim)
    v = np.hstack((first_row, data[:, 4])).reshape(dim)
    vel = np.array((u, v))
    return x, y, vel
