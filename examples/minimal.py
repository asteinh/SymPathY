from sympathy import ParsePaths
import matplotlib.pyplot as plt
import numpy as np

curve = \
    "M 0 0 " \
    "C 10,10 20,10 30,0 " \
    "Z"

path = ParsePaths(curve)[0]
for i in range(9):
    path.rotate(40)
    p = path.point(np.linspace(0, 1, 100))
    plt.plot(p[0, :], p[1, :])

plt.gca().invert_yaxis()
plt.axis('equal')
plt.show()
