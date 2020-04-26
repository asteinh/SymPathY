from svg2trajectory import Parser
import matplotlib
import matplotlib.pyplot as plt

import numpy as np

# get all paths in SVG as a list
paths = Parser('examples/svg/racetrack.svg')
path = paths[0]

print("Total path length: {}".format(path.length()))

N = 500
s = np.linspace(0, 1, N)

p = path.point(s)
c = path.curvature(s)

normalize = matplotlib.colors.SymLogNorm(linthresh=5e-3, vmin=np.min(c), vmax=np.max(c), base=10)
s = plt.scatter(p[0, :], p[1, :], c=c, s=20, cmap='RdYlGn', norm=normalize, marker='.', alpha=0.5, zorder=2)
cbar = plt.colorbar(s)
cbar.ax.set_ylabel('Curvature')

path.natural_parametrization()

N = 100
s = np.linspace(0, 1, N)

p = path.point(s)
t = 5*path.tangent(s)
n = 3*path.normal(s)

for i in range(N):
    plt.arrow(p[0, i], p[1, i], t[0, i], t[1, i], color='black', zorder=1)
    plt.arrow(p[0, i], p[1, i], n[0, i], n[1, i], color='gray', zorder=1)

plt.axis('equal')
# plt.grid()
plt.show()
