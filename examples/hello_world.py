from svg2trajectory import Parser
import matplotlib.pyplot as plt

# get all paths in SVG as a list
paths = Parser('examples/svg/hello_world.svg')
path = paths[0]

print(path.length())

N = 250
p = [path.point(i/N) for i in range(0, N)]
x = [p_[0] for p_ in p]
y = [p_[1] for p_ in p]
plt.plot(x, y, color='blue', linestyle='dotted')

N = 100
for i in range(0, N):
    s = i/N
    p = path.point(s)
    t = path.tangent(s, length=3)
    n = path.normal(s, length=3)
    plt.plot(p[0], p[1], 'r.')
    plt.arrow(p[0], p[1], t[0], t[1], color='red')
    plt.arrow(p[0], p[1], n[0], n[1], color='green')

plt.show()
