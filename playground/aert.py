import matplotlib.pyplot as plt
import numpy as np
from numpy import ma

X, Y = np.meshgrid(np.arange(0, 2 * np.pi, .2), np.arange(0, 2 * np.pi, .2))
U = np.cos(X)
V = np.sin(Y)
skip=(slice(None,None,3),slice(None,None,3))


plt.figure()
plt.title('Arrows scale with plot width, not view')
Q = plt.quiver(X[skip], Y[skip], U[skip], V[skip], units='width')
qk = plt.quiverkey(Q, 0.9, 0.9, 1, r'$1 \frac{m}{s}$', labelpos='E',
                   coordinates='figure')

#quiver(x(1:2:end,1:2:end),y(1:2:end,1:2:end),u(1:2:end,1:2:end),v(1:2:end,1:2:end))
plt.show()
