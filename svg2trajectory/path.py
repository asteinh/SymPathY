from svg.path import Path
from svg2trajectory.elements import SymbolicMixin
from svg2trajectory.elements import SymbolicMove, SymbolicLine, SymbolicCubicBezier
import casadi as cas
import numpy as np


class SymbolicPath(SymbolicMixin, Path):
    def __init__(self, path):
        Path.__init__(self)
        SymbolicMixin.__init__(self)

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

    def tangent(self, s=None):
        # unit tangent vector
        dp_ds = cas.jacobian(self._expr, self._s)
        tangent = dp_ds / cas.norm_2(dp_ds)
        if s is None:
            return tangent
        else:
            t = cas.Function('tangent', [self._s], [tangent])
            return np.array(t(s)).flatten()

    def normal(self, s=None):
        # unit normal vector
        dt_ds = cas.jacobian(self.tangent(), self._s)
        normal = dt_ds/cas.norm_2(dt_ds)
        if s is None:
            return normal
        else:
            n = cas.Function('normal', [self._s], [normal])
            return np.array(n(s)).flatten()

    def curvature(self, s):
        # curvature value
        dp_ds = cas.jacobian(self._expr, self._s)
        dt_ds = cas.jacobian(self.tangent(), self._s)
        kappa = cas.norm_2(dt_ds) / cas.norm_2(dp_ds)
        if s is None:
            return kappa
        else:
            k = cas.Function('kappa', [self._s], [kappa])
            return np.float(k(s))

    # def resize(self, start=[0, 0], end=[1, None]):
    #     pass
    #
    # def rotate(self, angle):
    #     pass
