from svg.path import Path
from svg2trajectory.elements import *
import casadi as cas
from bisect import bisect


class SymbolicPath(Path):
    def __init__(self, path):
        super().__init__()
        for e in path._segments:
            c = 'Symbolic' + e.__class__.__name__
            self._segments.append(globals()[c](e))

    def _calc_lengths(self, **kwargs):
        if self._length is not None:
            return

        lengths = [seg.length() for seg in self._segments]
        self._length = sum(lengths)
        self._lengths = [each / self._length for each in lengths]
        fraction = 0
        for each in self._lengths:
            fraction += each
            self._fractions.append(fraction)

    def point(self, s):
        p = Path.point(self, s)
        return [float(p[0]), float(p[1])]

    def length(self):
        self._calc_lengths()
        return float(self._length)

    def derivative(self, s, length=None):
        self._calc_lengths()
        i = bisect(self._fractions, s)
        seg = self._segments[i]
        deriv = cas.Function('deriv', [seg._s], [cas.jacobian(seg._expr, seg._s)])
        d = deriv(s)

        if length:
            d /= cas.sqrt(cas.sum1(d[0]**2 + d[1]**2))
            d *= length

        return [float(d[0]), float(d[1])]

    # TODO
    def resize(self, start=[0, 0], end=[1, None]):
        pass

    # TODO
    def rotate(self, angle):
        pass
