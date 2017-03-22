# loading of the experimental data
# importing modules
import numpy as np
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm
import vortex_detection

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
        vel (np.array : shape (3, # x dof, # y dof)) = vel[0,i,j] is the u of the point_ij and v[1,i,j] is the v of point_ij ...

    """
    try:
        if experiment not in ['16', '04']:
            raise ValueError()
    except ValueError:
        print("Choose between '16' or '04'")
    data = np.loadtxt(dir_path + "/../exp_data/Velocity_" + experiment + ".plt", skiprows=4)
    # select columns data reppresenting position
    position = data[:, :2]
    velocity = remove_zeros(data[:, 3:])
    x, y, dim = parse_structured_grid(position)
    # data is missing one row
    first_row = np.array((0))
    # stack missing row and reshape according to the dimensions of the grid
    u = np.hstack((first_row, velocity[:, 0])).reshape(dim)
    v = np.hstack((first_row, velocity[:, 1])).reshape(dim)
    w = np.hstack((first_row, velocity[:, 2])).reshape(dim)
    vel = np.array((u, v, w))
    return x, y, vel


def remove_zeros(velocity):
    for i in range(np.shape(velocity)[1]):
        mask = np.where(velocity[:, i] == 0)
        velocity[mask, i] = np.nan
    return velocity


def plot_data_3d(xx, yy, data, save=False, show=True, *args):
    """Plot interpolant function.

    Args:
        xx (np.array) = array of x coordinated created through meshgrid
        yy (np.array) = array of y coordinated created through meshgrid
        radial func (obj func) = radial function
        l (float) = parameter for sharpness of radial func.

    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    p = ax.plot_surface(xx, yy, data, rstride=1, cstride=1, linewidth=0,
                        cmap=cm.bone, vmin=np.nanmin(data), vmax=np.nanmax(data))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    fig.colorbar(p)
    # Set rotation angle to 30 degrees
    ax.view_init(azim=70)
    # for angle in range(0, 360):
    #     ax.view_init(30, angle)
    #     plt.draw()
    if args:
        ax.set_title(args[0])
        ax.set_zlabel(args[1])
    if save:
        plt.savefig(dir_path + '/../images/' + args[0] + '.png', bbox_inches='tight')
    plt.show()


def countour_data_plot(xx, yy, data, *args, save=False, show=True):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    cs = plt.contourf(xx, yy, data, 10, cmap=cm.bone, origin='lower')
    ax.set_xlabel('x')
    # ax.set_ylabel('y')
    fig.colorbar(cs)
    print(args)
    if args:
        ax.set_title(args[0])
        ax.set_ylabel(args[1])
    if save and args:
        plt.savefig(dir_path + '/../images/' + args[0] + '.png', bbox_inches='tight')
    if show:
        plt.show()

def vortexcenter_scatter_plot(xx, yy, data, centers, *args, save=False, show=True, new_plot=True):
    if new_plot:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111)
        cs = plt.contourf(xx, yy, data, 10, cmap=cm.bone, origin='lower')
        fig.colorbar(cs)
        ax.set_xlabel('x')

    xlst = []
    ylst = []
    strengthlst = []
    for point in centers:
        i,j,strength = point
        x = xx[i, j]
        y = yy[i, j]
        strengthlst.append(strength*100)
        xlst.append(x)
        ylst.append(y)

    plt.scatter(xlst,ylst, s = strengthlst)

    # ax.set_ylabel('y')
    if args:
        ax.set_title(args[0])
        ax.set_ylabel(args[1])
    if save and args:
        plt.savefig(dir_path + '/../images/' + args[0] + '.png', bbox_inches='tight')
    if show:
        plt.show()



def quiver_data_plot(xx, yy, data, plane_vector, *args, vortex_centers = None, save=False, show=True):
    """Quiver plot."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    cs = plt.contourf(xx, yy, data, 10, cmap=cm.bone, origin='lower')
    mag_plane_vel = (plane_vector[0, :, :] ** 2 + plane_vector[1, :, :] ** 2) ** 0.5
    max = np.nanmax(mag_plane_vel)
    Q = plt.quiver(xx, yy, plane_vector[0], plane_vector[1], units='width', pivot='tip', scale=5)
    qk = plt.quiverkey(Q, 0.9, 0.9, max, r'{0:.2f} m/s' .format(max), labelpos='E',
                       coordinates='figure')
    if vortex_centers:
        vortexcenter_scatter_plot(xx,yy,data,vortex_centers, show=False, new_plot=False)
    ax.set_xlabel('x')
    # ax.set_ylabel('y')
    fig.colorbar(cs)
    print(args)
    if args:
        ax.set_title(args[0])
        ax.set_ylabel(args[1])
    if save and args:
        plt.savefig(dir_path + '/../images/' + args[0] + '.png', bbox_inches='tight')
    if show:
        plt.show()

if __name__ == '__main__':
    pass
    # x, y, vel = load_data('16')
    # xx, yy = np.meshgrid(x, y)
    # print(vel[2, :, :])
    # # plot_data_3d(xx, yy, vel[0, :, :])
    # countour_data_plot(xx, yy, vel[0, :, :])
    # countour_data_plot(xx, yy, vel[1, :, :])
    # countour_data_plot(xx, yy, vel[2, :, :])
