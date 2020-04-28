from sympathy import ParsePaths
import matplotlib.pyplot as plt
import numpy as np

paths = ParsePaths('tests/files/all_types.svg')
for i, path in enumerate(paths):
    # if i == 1:
    #     path.natural_parametrization()

    print("Total path length: {}".format(path.length()))

    if path.length() > 100:
        N = 40
    else:
        N = 20
    s = np.linspace(0, 1, N)
    p = path.point(s)
    t = 10*path.tangent(s)
    n = 2*path.normal(s)

    plt.plot(p[0, :], p[1, :], 'r-', zorder=2)

    for k in range(0, N, 1):
        plt.arrow(p[0, k], p[1, k], t[0, k], t[1, k], color='black', alpha=0.5, zorder=1)
        plt.arrow(p[0, k], p[1, k], n[0, k], n[1, k], color='black', alpha=0.25, zorder=1)

plt.gca().invert_yaxis()
plt.axis('equal')
plt.grid()
plt.show()
