#loading of the experimental data
#importing modules
import pickle
std_vel04 = open('exp_data\StD_vel04.plt', 'rb')
std_vel04f = pickle.load(std_vel04)
print (std_vel04f)
