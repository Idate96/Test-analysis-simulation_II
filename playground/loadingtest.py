import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
data = np.loadtxt('exp_data_kopie\StD_vel04(1).plt')
xtab=[]
ytab=[]
xtab1=[]
ytab1=[]
xtab2=[]
ytab2=[]
for i in range(len(data)):
    xtab.append(data[i][3])
    ytab.append((data[i][3])/sqrt(500))
    xtab1.append(data[i][4])
    ytab1.append((data[i][4])/sqrt(500))
    xtab1.append(data[i][5])
    ytab1.append((data[i][5])/sqrt(500))

plt.plot(xtab,ytab, "bo",xtab,ytab, "r--", xtab,ytab, "bo")
plt.show()
