from svg.path import Line, CubicBezier, Move, Close
import casadi as cas


class SymbolicMixin(object):
    def __init__(self):
        self._s = cas.SX.sym('s')
        self._expr = cas.SX.nan(2, 1)

    def arclength(self, s):
        # arc length for s \in [0,1]
        deriv = cas.jacobian(self._expr, self._s)
        length = cas.integrator(
            'integrator',
            'rk',
            {'x': cas.SX.sym('null'), 't': self._s, 'ode': 0, 'quad': cas.norm_2(deriv)},
            {'t0': 0.0, 'tf': s}
        ).call({})['qf']
        return length


class SymbolicElement(SymbolicMixin):
    def __init__(self, base):
        SymbolicMixin.__init__(self)
        self.start = cas.DM([base.start.real, -base.start.imag])
        self.end = cas.DM([base.end.real, -base.end.imag])
        self._expr = self.point(self._s)


class SymbolicLine(SymbolicElement, Line):
    def __init__(self, base):
        SymbolicElement.__init__(self, base)

    def length(self, **kwargs):
        return float(cas.norm_2(self.end-self.start))


class SymbolicCubicBezier(SymbolicElement, CubicBezier):
    def __init__(self, base):
        self.control1 = cas.DM([base.control1.real, -base.control1.imag])
        self.control2 = cas.DM([base.control2.real, -base.control2.imag])
        SymbolicElement.__init__(self, base)

    def length(self, **kwargs):
        return float(self.arclength(1.0))


# class SymbolicQuadraticBezier(SymbolicElement, QuadraticBezier):
#     def __init__(self, base):
#         SymbolicElement.__init__(self, base)
#
#         self.control = cas.DM([base.control.real, -base.control.imag])
#         self._expr = self.point(self._s)


# class SymbolicArc(SymbolicElement, Arc):
#     def __init__(self, base):
#         SymbolicElement.__init__(self, base)
#
#         self._expr = self.point(self._s)


class SymbolicMove(SymbolicElement, Move):
    def __init__(self, base):
        SymbolicElement.__init__(self, base)

    def length(self, **kwargs):
        return 0.0


class SymbolicClose(SymbolicElement, Close):
    def __init__(self, base):
        SymbolicElement.__init__(self, base)

    def length(self, **kwargs):
        return 0.0
