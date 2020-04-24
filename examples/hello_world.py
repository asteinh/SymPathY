from svg2trajectory import Parser
import matplotlib
import matplotlib.pyplot as plt

# get all paths in SVG as a list
paths = Parser('examples/svg/hello_world.svg')
path = paths[0]

print("Total path length: {}".format(path.length()))

N = 1000
p = [(path.point(i/N), path.curvature(i/N)) for i in range(0, N)]
x = [p_[0][0] for p_ in p]
y = [p_[0][1] for p_ in p]
k = [p_[1] for p_ in p]

normalize = matplotlib.colors.SymLogNorm(linthresh=1e-6, vmin=min(k[1:]), vmax=max(k[1:]), base=10)
plt.scatter(x, y, c=k, s=3, cmap='RdYlGn', norm=normalize, marker='+')

N = 100
for i in range(0, N):
    s = i/N
    p = path.point(s)
    t = 2*path.tangent(s)
    n = 2*path.normal(s)

    # plt.plot(p[0], p[1], 'r.', zorder=1)
    plt.arrow(p[0], p[1], t[0], t[1], color='blue', zorder=2)
    plt.arrow(p[0], p[1], n[0], n[1], color='green', zorder=2)

plt.show()
