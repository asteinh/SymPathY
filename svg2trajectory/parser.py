import xml.etree.ElementTree as et
from svg.path import parse_path
from svg2trajectory.path import SymbolicPath
import re


class Parser():
    def __init__(self, svg_file):
        self.svg_file = svg_file
        xml = et.parse(svg_file)
        xml_paths = xml.getroot().findall(".//{http://www.w3.org/2000/svg}path")
        self.__parse_all(xml_paths=xml_paths)

    def __parse_all(self, xml_paths):
        self.paths = []
        for xml in xml_paths:
            path = self.__parse_path(xml)
            transforms = self.__parse_transforms(xml)
            for t in reversed(transforms):
                getattr(path, t['type'])(**t['kwargs'])
            self.paths.append(path)

    def __parse_path(self, xml):
        str = xml.get('d')
        return SymbolicPath(parse_path(str))

    def __parse_transforms(self, xml):
        str = xml.get('transform')
        res = []
        if not str:
            return []

        for match in re.finditer("([a-zA-Z]*)\\((.*?)\\)", str):
            transform = match.groups()[0]
            argstr = match.groups()[1]

            if transform == 'translate':
                vals = re.findall("(-?\\d+\\.?\\d*)", argstr)
                if len(vals) == 2:
                    res.append({'type': 'translate', 'kwargs': {'dx': float(vals[0]), 'dy': float(vals[1])}})
                else:
                    res.append({'type': 'translate', 'kwargs': {'dx': float(vals[0]), 'dy': 0.0}})

            elif transform == 'rotate':
                vals = re.findall("(-?\\d+\\.?\\d*)", argstr)
                if len(vals) == 3:
                    res.append({
                        'type': 'rotate',
                        'kwargs': {'theta': float(vals[0]), 'x': float(vals[1]), 'y': float(vals[2])}
                    })
                else:
                    res.append({'type': 'rotate', 'kwargs': {'theta': float(vals[0]), 'x': 0.0, 'y': 0.0}})

            else:
                # TODO parse other transformations
                pass

        return res

    def __getitem__(self, index):
        return self.paths[index]
