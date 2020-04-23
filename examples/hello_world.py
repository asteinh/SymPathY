from svg2trajectory import Parser
import matplotlib.pyplot as plt

# get all paths in SVG as a list
paths = Parser('examples/svg/hello_world.svg')
path = paths[0]

N = 100
for i in range(0, N):
    s = i/N
    p = path.point(s)
    d = path.derivative(s, length=3)
    plt.plot(p[0], p[1], 'b.')
    plt.arrow(p[0], p[1], d[0], d[1], color='red')

plt.show()
