import xml.etree.ElementTree as et
from svg.path import parse_path

class Parser():
    def __init__(self, svg_file):
        xml = et.parse(svg_file)
        self.paths = xml.getroot().findall(".//{http://www.w3.org/2000/svg}path")

    def sample_paths(self, n=100, start=[0,0], end=[1,None]):
        paths = []
        for xml_path in self.paths:
            p = parse_path(xml_path.get('d'))
            t = [p.point(s/n) for s in range(0,n)]

            x_orig = [x.real for x in t]
            dx_orig = x_orig[-1] - x_orig[0]
            y_orig = [-y.imag for y in t]
            dy_orig = y_orig[-1] - y_orig[0]

            dx_mod = end[0] - start[0]
            if not end[1]:
                # scale like original
                end[1] = end[0] + dx_mod*dy_orig/dx_orig
                if y_orig[-1] < y_orig[0]:
                    end[1] *= -1
            dy_mod = end[1] - start[1]

            x_mod = [(x-x_orig[0])/dx_orig*dx_mod + start[0] for x in x_orig]
            y_mod = [(y-y_orig[0])/dy_orig*dy_mod + start[1] for y in y_orig]

            paths.append({ 'x': x_mod, 'y': y_mod })

        return paths
