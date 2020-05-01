from sympathor import ParsePaths
import matplotlib.pyplot as plt
import numpy as np

paths = ParsePaths('examples/files/pairs_of_paths.svg')
for i, path in enumerate(paths):

    print("Total path length: {}".format(path.length()))

    if i % 2 == 1:
        path.set_natural_parametrization(True)
        col = 'r'
    else:
        col = 'b'

    N = 50
    s = np.linspace(0, 1, N)
    p = path.point(s)

    plt.plot(p[0, :], p[1, :], col+'.', zorder=1)

plt.gca().invert_yaxis()
plt.axis('equal')
plt.grid()
plt.show()
