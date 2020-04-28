from sympathor import ParsePaths
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

paths = ParsePaths('examples/racetrack/Spa-Francorchamps.svg')

print("Found a total of {} paths.".format(len(paths)))

circuit = paths[2]
# pitlane = paths[3]

N = 250
s = np.linspace(0, 1, N)
p = circuit.point(s)
t = circuit.tangent(s)
n = circuit.normal(s)
c = circuit.curvature(s)

normalize = matplotlib.colors.SymLogNorm(linthresh=1e-3, vmin=np.min(c), vmax=np.max(c), base=10)

s = plt.scatter(p[0, :], p[1, :], c=c, s=25, cmap='RdYlGn_r', norm=normalize, marker='.', alpha=0.9, zorder=2)
cbar = plt.colorbar(s)
cbar.ax.set_ylabel('Curvature')

for i in range(N):
    plt.arrow(p[0, i], p[1, i], 10*t[0, i], 10*t[1, i], color='black', zorder=1)
    plt.arrow(p[0, i], p[1, i], 10*n[0, i], 10*n[1, i], color='gray', zorder=1)

plt.gca().invert_yaxis()
plt.axis('equal')
plt.grid()
plt.show()
