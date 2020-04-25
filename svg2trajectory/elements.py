from svg.path import Line, CubicBezier, Move, Close
import casadi as cas


def quadrature(fcn, a, b, N=100):
    # Simpson's rule
    N += 1 if N % 2 != 0 else 0
    fcnmap = fcn.map(N+1)
    xvals = cas.linspace(a, b, N+1)
    fvals = fcnmap(xvals)
    return (b-a)/N/3 * (fvals[0] + 4*cas.sum2(fvals[1::2]) + 2*cas.sum2(fvals[2:-2:2]) + fvals[-1])


class SymbolicMixin(object):
    def __init__(self):
        self._s = cas.SX.sym('s')
        self._expr = cas.SX.nan(2, 1)

    def arclength(self, s):
        length = cas.integrator(
            'integrator',
            'rk',
            {'x': cas.SX.sym('null'), 't': self._s, 'ode': 0, 'quad': cas.norm_2(cas.jacobian(self._expr, self._s))},
            {'t0': 0.0, 'tf': s}
        ).call({})['qf']
        return length


class SymbolicElement(SymbolicMixin):
    def __init__(self, base, expr_from=None):
        SymbolicMixin.__init__(self)
        self.start = cas.DM([base.start.real, -base.start.imag])
        self.end = cas.DM([base.end.real, -base.end.imag])
        if expr_from:
            self._expr = expr_from(self, self._s)
        else:
            self._expr = self.point(self._s)
        self._tangent = cas.jacobian(self._expr, self._s)
        self._tangent_norm = cas.norm_2(self._tangent)

    def arclength(self, s):
        # approximation of arc length for elements
        fcn = cas.Function('fcn', [self._s], [self._tangent_norm])
        return quadrature(fcn, 0.0, s)


class SymbolicLine(SymbolicElement, Line):
    def __init__(self, base):
        SymbolicElement.__init__(self, base)

    def length(self, **kwargs):
        return float(cas.norm_2(self.end-self.start))


class SymbolicCubicBezier(SymbolicElement, CubicBezier):
    def __init__(self, base):
        self.control1 = cas.DM([base.control1.real, -base.control1.imag])
        self.control2 = cas.DM([base.control2.real, -base.control2.imag])
        SymbolicElement.__init__(self, base, expr_from=CubicBezier.point)

        self._rescaler = self._setup_rescaler()

    def _setup_rescaler(self):
        # find a point where arc length == s * length
        s_noli = cas.SX.sym('s_noli')
        fcn = cas.Function('fcn', [self._s, s_noli], [self.arclength(self._s) - s_noli*self.length()])
        return cas.rootfinder('r', 'newton', fcn)

    def s_linear_scale(self, s):
        return self._rescaler(s, s)

    def point(self, s):
        return CubicBezier.point(self, self.s_linear_scale(s))

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
#     def length(self, **kwargs):
#         return float(self.arclength(1.0))


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
