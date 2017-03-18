"""this is task number 2."""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np

print("here is where the magic will happen")
TestList = [[(0.2, 0.2, 0, 0, 0, 0), (0.4, 0.2, 0, 1, 0, 0), (0.6, 0.2, 0, 2, 0, 0), (0.8, 0.2, 0, 1, 0, 0), (1.0, 0.2, 0, 0, 0, 0)], [(0.2, 0.4, 0, 1, 0, 0), (0.4, 0.4, 0, 2, 0, 0), (0.6, 0.4, 0, 3, 0, 0), (0.8, 0.4, 0, 2, 0, 0), (1.0, 0.4, 0, 1, 0, 0)], [(0.2, 0.6, 0, 2, 0, 0), (0.4, 0.6, 0, 3, 0, 0), (0.6, 0.6, 0, 4, 0, 0), (0.8, 0.6, 0, 3, 0, 0), (1.0, 0.6, 0, 2, 0, 0)], [(0.2, 0.6, 0, 2, 0, 0), (), (), (), ()], [(), (), (), (), ()]]

def Make_TestList():
    """
    This function makes a testlist that consists of 5 lists, each with 5 tuples
    to represent the data received by 1.

    takes in nothing, starts at the origin with steps of 0.2 till 1
    """

    def tuple_returner(i, j):
        return (i * 0.2, j * 0.2, 0, i+j, 0, 0)

    ans = []
    for j in range(6):
        semi_ans = []
        for i in range(6):
            semi_ans.append(tuple_returner(i, j))
        ans.append(semi_ans)

    return ans




print("Here we gooo!!!")
# we should know what data structure we receive
# with that we can work to get the components of the velocity at different
# points
# the main task is to get the freestream component of the flow and divide it by
# the freestream velocity
# then we can make a clear conclusion between 4 and 16 m/s about the viscosity
# This can be done using a planar graph of the velocity and let them intersect
# eachother
