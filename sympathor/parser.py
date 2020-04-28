import xml.etree.ElementTree as et
from svg.path import parse_path
from sympathor.path import SymbolicPath
import os.path
import re


class ParsePaths():
    def __init__(self, input):
        raw_input = True
        file_input = False
        # check if input is valid file
        if os.path.exists(input):
            file_input = True
            try:
                xml = et.parse(input)
                raw_input = False
            except et.ParseError:
                # raise ValueError("The file referred to does not seem to be in XML format.") from exc
                pass

            if not raw_input:
                root = xml.getroot()
                # check if file is an SVG
                if root.tag == '{http://www.w3.org/2000/svg}svg':
                    xml_paths = root.findall(".//{http://www.w3.org/2000/svg}path")
                    self.__parse_paths_from_xml(xml_paths=xml_paths)

                # or try to parse path element
                elif root.tag == 'path':
                    self.__parse_paths_from_xml(xml_paths=[root])

                else:
                    raise ValueError("The content of the file referred to could not be interpreted.")

        # check if input is a path element
        if raw_input:
            if file_input:
                input_ = open(input).read()
            else:
                input_ = input
            xml_paths = self.__xml_from_raw(input_)
            self.__parse_paths_from_xml(xml_paths=xml_paths)

    def __xml_from_raw(self, input_):
        input = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" \
              + "<svg xmlns=\"http://www.w3.org/2000/svg\"><path d=\"" + input_ + "\" /></svg>"
        try:
            root = et.fromstring(input)
        except et.ParseError as exc:
            raise ValueError("The input provided could not be interpreted.") from exc

        return root.findall(".//{http://www.w3.org/2000/svg}path")

    def __parse_paths_from_xml(self, xml_paths):
        self.paths = []
        for xml in xml_paths:
            desc = parse_path(xml.get('d'))
            path = SymbolicPath(desc)
            transform = self.__parse_transform_from_xml(xml)
            for t in reversed(transform):
                getattr(path, t['type'])(**t['kwargs'])
            self.paths.append(path)

    def __parse_transform_from_xml(self, xml):
        str = xml.get('transform')
        res = []
        if not str:
            return []

        for match in re.finditer("([a-zA-Z]*)\\((.*?)\\)", str):
            transform = match.groups()[0]
            argstr = match.groups()[1]

            if transform == 'matrix':
                vals = re.findall("(-?\\d+\\.?\\d*)", argstr)
                res.append({
                    'type': 'matrix',
                    'kwargs': {
                        'a': float(vals[0]), 'b': float(vals[1]), 'c': float(vals[2]),
                        'd': float(vals[3]), 'e': float(vals[4]), 'f': float(vals[5])
                    }
                })

            elif transform == 'translate':
                vals = re.findall("(-?\\d+\\.?\\d*)", argstr)
                if len(vals) == 2:
                    res.append({'type': 'translate', 'kwargs': {'dx': float(vals[0]), 'dy': float(vals[1])}})
                else:
                    res.append({'type': 'translate', 'kwargs': {'dx': float(vals[0])}})

            elif transform == 'rotate':
                vals = re.findall("(-?\\d+\\.?\\d*)", argstr)
                if len(vals) == 3:
                    res.append({
                        'type': 'rotate',
                        'kwargs': {'theta': float(vals[0]), 'x': float(vals[1]), 'y': float(vals[2])}
                    })
                else:
                    res.append({'type': 'rotate', 'kwargs': {'theta': float(vals[0])}})

            elif transform == 'scale':
                vals = re.findall("(-?\\d+\\.?\\d*)", argstr)
                if len(vals) == 2:
                    res.append({'type': 'scale', 'kwargs': {'x': float(vals[0]), 'y': float(vals[1])}})
                else:
                    res.append({'type': 'scale', 'kwargs': {'x': float(vals[0])}})

            elif transform == 'skewX':
                vals = re.findall("(-?\\d+\\.?\\d*)", argstr)
                res.append({'type': 'skewX', 'kwargs': {'theta': float(vals[0])}})

            elif transform == 'skewY':
                vals = re.findall("(-?\\d+\\.?\\d*)", argstr)
                res.append({'type': 'skewY', 'kwargs': {'theta': float(vals[0])}})

            else:
                raise NotImplementedError

        return res

    def __getitem__(self, index):
        return self.paths[index]
