from svg.path import Path
from svg2trajectory.elements import *
import casadi as cas
import numpy as np
from bisect import bisect


class SymbolicPath(Path):
    def __init__(self, path):
        super().__init__()

        self._s = cas.SX.sym('s')

        # build path from segments
        for seg in path._segments:
            clss = 'Symbolic' + seg.__class__.__name__
            self._segments.append(globals()[clss](seg))

        # build composite symbolic expression
        self._expr = self._composite_path()

    def _composite_path(self):
        self._calc_lengths()
        expr = cas.SX.nan(2, 1)
        for i in range(len(self._segments)-1, -1, -1):
            s_max = self._fractions[i]
            if s_max <= 0.0:
                expr = cas.if_else(self._s < 0.0, cas.SX.nan(2, 1), expr)
                break
            else:
                s_min = self._fractions[i-1] if i > 0 else 0
                s_loc = (self._s - s_min) / self._lengths[i]
                fcn = cas.Function('seg', [self._segments[i]._s], [self._segments[i]._expr])
                expr = cas.if_else(self._s <= s_max, fcn(s_loc), expr)
        return expr

    def point(self, s):
        p = Path.point(self, s)
        return np.array(p).flatten()

    def length(self):
        return np.float(Path.length(self))

    def tangent(self, s, length=1):
        dp_ds = cas.Function('dp_ds', [self._s], [cas.jacobian(self._expr, self._s)])
        t = dp_ds(s)
        if length:
            t *= length / cas.sqrt(cas.sum1(t[0]**2 + t[1]**2))
        return np.array(t).flatten()

    def normal(self, s, length=1):
        dp_ds = cas.Function('dp_ds', [self._s], [cas.jacobian(self._expr, self._s)])
        ddp_dds = cas.Function('ddp_dds', [self._s], [cas.jacobian(dp_ds(self._s), self._s)])
        t = self.tangent(s, length=1)
        n = ddp_dds(s) - cas.dot(ddp_dds(s), t) * t
        if length:
            n *= length / cas.sqrt(cas.sum1(n[0]**2 + n[1]**2))
        return np.array(n).flatten()

    # def curvature(self, s):
    #     t = self.tangent(s, length=None)
    #     kappa = cas.dot()/cas.sqrt(cas.sum1(t[0]**2 + t[1]**2))

    # TODO
    def resize(self, start=[0, 0], end=[1, None]):
        pass

    # TODO
    def rotate(self, angle):
        pass
