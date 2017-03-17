#loading of the experimental data
#importing modules
import numpy as np

#loading the data (StD_vel04)

location = 'exp_data_kopie\StD_vel04.plt'
def load(x,y,location):
    data = np.loadtxt(loc)
    numb_loc = y*64 + x
    return data[numb_loc]

print(load(0,0,loc))


#matrix[0]=[1,1,1,1,1,1]
#print(matrix)
#data = np.loadtxt('exp_data_kopie\StD_vel04.plt')
#print(data)
