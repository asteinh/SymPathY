from sympathor import ParsePaths
import matplotlib.pyplot as plt
import numpy as np

paths = ParsePaths('examples/files/two_cubic_beziers.svg')
for i, path in enumerate(paths):
    if i == 1:
        path.natural_parametrization()

    print("Total path length: {}".format(path.length()))

    N = 50
    s = np.linspace(0, 1, N)
    p = path.point(s)

    plt.plot(p[0, :], p[1, :], 'r.', zorder=1)

plt.gca().invert_yaxis()
plt.axis('equal')
plt.grid()
plt.show()
