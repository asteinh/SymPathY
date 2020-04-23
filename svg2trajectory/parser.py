import xml.etree.ElementTree as et
from svg.path import parse_path
from svg2trajectory.path import SymbolicPath


class Parser():
    def __init__(self, svg_file):
        self.svg_file = svg_file
        xml = et.parse(svg_file)
        xml_paths = xml.getroot().findall(".//{http://www.w3.org/2000/svg}path")
        self.parse_all(xml_paths=xml_paths)

    def parse_all(self, xml_paths):
        self.paths = []
        for xml in xml_paths:
            p = parse_path(xml.get('d'))
            self.paths.append(SymbolicPath(p))

    def __getitem__(self, index):
        return self.paths[index]
