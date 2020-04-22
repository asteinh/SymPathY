from svg2trajectory import Parser

parser = Parser('examples/svg/hello_world.svg')
path = parser.sample_paths()

import matplotlib.pyplot as plt
for p in path:
    plt.plot(p['x'], p['y'], 'b')

plt.show()
