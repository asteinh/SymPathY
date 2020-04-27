from svg.path import Path
from svg2trajectory.elements import SymbolicMixin
import svg2trajectory.elements as elements
# , SymbolicMove, SymbolicLine, SymbolicCubicBezier  # noqa: F401
# from svg2trajectory.elements import SymbolicQuadraticBezier, SymbolicArc, SymbolicClose  # noqa: F401
import casadi as cas
import numpy as np


class SymbolicPath(SymbolicMixin, Path):
    def __init__(self, path):
        Path.__init__(self)
        SymbolicMixin.__init__(self)

        # build path from segments
        for seg in path._segments:
            clss = 'Symbolic' + seg.__class__.__name__
            self._segments.append(getattr(elements, clss)(seg))

        self.__symbolic_setup()

    def __symbolic_setup(self):
        # build composite symbolic expression
        self._calc_lengths()
        expr = cas.MX.nan(2, 1)
        for i in range(len(self._segments)-1, -1, -1):
            s_max = self._fractions[i]
            if s_max <= 0.0:
                expr = cas.if_else(self._s < 0.0, cas.MX.nan(2, 1), expr)
                break
            else:
                s_min = self._fractions[i-1] if i > 0 else 0
                s_loc = (self._s - s_min) / self._lengths[i]
                expr = cas.if_else(self._s <= s_max, self._segments[i].point(s_loc), expr)
        self._point_expr = expr
        self._point = cas.Function('point', [self._s], [self._point_expr])

        dp_ds = cas.jacobian(self._point_expr, self._s)
        # unit tangent vector
        self._tangent_expr = dp_ds / cas.norm_2(dp_ds)
        self._tangent = cas.Function('tangent', [self._s], [self._tangent_expr])
        dt_ds = cas.jacobian(self._tangent_expr, self._s)
        # unit normal vector
        self._normal_expr = dt_ds / cas.norm_2(dt_ds)
        self._normal = cas.Function('normal', [self._s], [self._normal_expr])
        # curvature value
        self._curvature_expr = cas.norm_2(dt_ds) / cas.norm_2(dp_ds)
        self._curvature = cas.Function('curvature', [self._s], [self._curvature_expr])

    def __maybe_map_function(self, fcn, s):
        s_ = np.asarray(s).flatten()
        N = np.size(s_)
        fcn_ = fcn.map(N) if N > 1 else fcn
        return fcn_(s_)

    def natural_parametrization(self, on=True):
        if on:
            for seg in self._segments:
                seg._natural_parametrization = True
        else:
            for seg in self._segments:
                seg._natural_parametrization = False
        self.__symbolic_setup()

    def length(self):
        return np.float(Path.length(self))

    def point(self, s=None):
        if s is None:
            return self._point_expr
        else:
            p = self.__maybe_map_function(self._point, s)
            return np.array(p)

    def tangent(self, s=None):
        if s is None:
            return self._tangent_expr
        else:
            t = self.__maybe_map_function(self._tangent, s)
            return np.array(t)

    def normal(self, s=None):
        if s is None:
            return self._normal_expr
        else:
            n = self.__maybe_map_function(self._normal, s)
            return np.array(n)

    def curvature(self, s=None):
        if s is None:
            return self._curvature_expr
        else:
            c = self.__maybe_map_function(self._curvature, s)
            return np.array(c)

    # transforms
    def translate(self, dx, dy=0):
        for seg in self._segments:
            seg.translate(dx=dx, dy=dy)
        self.__symbolic_setup()

    def rotate(self, theta, x=0, y=0):
        for seg in self._segments:
            seg.rotate(theta=theta, x=x, y=y)
        self.__symbolic_setup()

    # def resize(self, start=[0, 0], end=[1, None]):
    #     pass
    #
    # def rotate(self, angle):
    #     pass
