#loading of the experimental data
#importing modules
import numpy as np

#loading the data (StD_vel04)
def load(x,y,location):
    #for location fill in the corresponding value in brackets in exp_data_kopie
    #0<=x<=64
    #0<=x<=64
    if location==1:
        location = 'exp_data_kopie\StD_vel04(1).plt'
    if location==2:
        location = 'exp_data_kopie\StD_vel16(2).plt'
    if location==3:
        location = 'exp_data_kopie\Velocity_04(3).plt'
    if location==4:
        location = 'exp_data_kopie\Velocity_16(4).plt'
    data = np.loadtxt(location)
    numb_loc = y*53 + x
    return data[numb_loc]



#example how to use it:
print(load(0,0,1))
#this will print the first row
