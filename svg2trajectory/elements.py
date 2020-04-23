from svg.path import Line, CubicBezier, Move
import casadi as cas


class SymbolicMixin():
    def __init__(self, base):
        self._s = cas.SX.sym('s')
        self.start = cas.DM([base.start.real, -base.start.imag])
        self.end = cas.DM([base.end.real, -base.end.imag])


class SymbolicLine(SymbolicMixin, Line):
    def __init__(self, base):
        super().__init__(base)
        self._expr = super().point(self._s)

    def length(self):
        return float(cas.sqrt(cas.sum1((self.end-self.start)**2)))


class SymbolicCubicBezier(SymbolicMixin, CubicBezier):
    def __init__(self, base):
        super().__init__(base)
        self.control1 = cas.DM([base.control1.real, -base.control1.imag])
        self.control2 = cas.DM([base.control2.real, -base.control2.imag])
        self._expr = super().point(self._s)

    def arclength(self, s):
        # arc length for s \in [0,1]
        deriv = cas.jacobian(self._expr, self._s)

        integ = cas.integrator(
            'integrator',
            'cvodes',
            {'x': self._s, 'ode': 0, 'quad': cas.sqrt(deriv[0]**2 + deriv[1]**2)},
            {'t0': 0.0, 'tf': 1.0}
        )

        return integ.call({'x0': s, 'p': s})['qf']

    def length(self):
        return float(self.arclength(1.0))


# class SymbolicQuadraticBezier(SymbolicMixin, QuadraticBezier):
#     def __init__(self, base):
#         super().__init__(base)
#         self._expr = super().point(self._s)


# class SymbolicArc(SymbolicMixin, Arc):
#     def __init__(self, base):
#         super().__init__(base)
#         self._expr = super().point(self._s)


class SymbolicMove(SymbolicMixin, Move):
    def __init__(self, base):
        super().__init__(base)
        self._expr = super().point(self._s)


# class SymbolicClose(SymbolicMixin, Close):
#     def __init__(self, base):
#         super().__init__(base)
#         self._expr = super().point(self._s)
