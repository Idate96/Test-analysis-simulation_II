"""this file contains the xy plot of the velocity field and stuff."""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
from load_file import *
import vortex_detection
import vorticity_strain

if __name__ == '__another_toon_frederic_epic_file__':
    exp = '04'
    x, y, vel = load_data(exp)
    xx, yy = np.meshgrid(x, y)

#http://talk.maemo.org/showthread.php?t=93307
#http://www.robertocolistete.net/MatPlotLib/vectorfieldFxy.py
