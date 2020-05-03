from svg.path import Line, CubicBezier, QuadraticBezier, Arc, Move, Close
import casadi as cas


def quadrature(fcn, a, b, N=200):
    # Simpson's rule
    N += 1 if N % 2 != 0 else 0
    fcnmap = fcn.map(N+1)
    xvals = cas.linspace(a, b, N+1)
    fvals = fcnmap(xvals)
    return (b-a)/N/3 * (fvals[0] + 4*cas.sum2(fvals[1::2]) + 2*cas.sum2(fvals[2:-2:2]) + fvals[-1])


def _imag_to_coord(val):
    return cas.DM([val.real, val.imag])


class SymbolicMixin(object):
    def __init__(self):
        self._s = cas.MX.sym('s')
        self._expr = cas.MX.nan(2, 1)
        self._eps = 1e-12
        self.natural_parametrization = False

    def arclength(self, s):
        if s == 0:
            return 0.0
        length = cas.integrator(
            'integrator',
            'rk',
            {'x': cas.MX.sym('null'), 't': self._s, 'ode': 0, 'quad': cas.norm_2(cas.jacobian(self._expr, self._s))},
            {'t0': 0.0, 'tf': s}
        ).call({})['qf']
        return length


class SymbolicElement(SymbolicMixin):
    def __init__(self, base, expr_from=None):
        SymbolicMixin.__init__(self)
        self.start = _imag_to_coord(base.start)
        self.end = _imag_to_coord(base.end)
        self.points = ['start', 'end']
        self.params = []

        self._expr = self.point(self._s)
        self._rescaler = self._setup_rescaler()

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        for p in [*self.points, *self.params]:
            if cas.norm_fro(getattr(self, p) - getattr(other, p)) > self._eps:
                return False
        return True

    def _setup_rescaler(self):
        # find a point where arc length == s * length
        s_noli = cas.MX.sym('s_noli')
        fcn = cas.Function('fcn', [self._s, s_noli], [self.arclength(self._s) - s_noli*self.length()])
        return cas.rootfinder('r', 'newton', fcn)

    def set_natural_parametrization(self, set=False):
        self.natural_parametrization = set

    def arclength(self, s):
        # approximation of arc length for elements
        fcn = cas.Function('fcn', [self._s], [cas.norm_2(cas.jacobian(self._expr, self._s))])
        return quadrature(fcn, 0.0, s)

    def length(self, **kwargs):
        return cas.norm_2(self.end-self.start)

    # TRANSFORMS
    def matrix(self, a, b, c, d, e, f):
        rot = cas.vertcat(cas.horzcat(a, c), cas.horzcat(b, d))
        delta = cas.vertcat(e, f)
        for p in self.points:
            p_ = getattr(self, p)
            setattr(self, p, rot@p_ + delta)

    def translate(self, dx, dy=0):
        self.matrix(1, 0, 0, 1, dx, dy)

    def rotate(self, theta, x=0, y=0):
        self.translate(dx=-x, dy=-y)
        self.matrix(
            +cas.cos(theta / 180 * cas.pi), +cas.sin(theta / 180 * cas.pi),
            -cas.sin(theta / 180 * cas.pi), +cas.cos(theta / 180 * cas.pi),
            x, y
        )

    def scale(self, x, y=None):
        if y is None:
            y = x
        self.matrix(x, 0, 0, y, 0, 0)

    def skewX(self, theta):
        tan = cas.tan(theta / 180 * cas.pi)
        self.matrix(1, 0, tan, 1, 0, 0)

    def skewY(self, theta):
        tan = cas.tan(theta / 180 * cas.pi)
        self.matrix(1, tan, 0, 1, 0, 0)


class SymbolicLine(SymbolicElement, Line):
    def __init__(self, base):
        SymbolicElement.__init__(self, base)


class SymbolicCubicBezier(SymbolicElement, CubicBezier):
    def __init__(self, base):
        self.control1 = _imag_to_coord(base.control1)
        self.control2 = _imag_to_coord(base.control2)
        SymbolicElement.__init__(self, base)
        self.points.extend(['control1', 'control2'])
        self.params.append('natural_parametrization')

    def point(self, s):
        if self.natural_parametrization:
            s = self._rescaler(s, s)
        return CubicBezier.point(self, s)

    def length(self, **kwargs):
        return self.arclength(1.0)


class SymbolicQuadraticBezier(SymbolicElement, QuadraticBezier):
    def __init__(self, base):
        self.control = _imag_to_coord(base.control)
        SymbolicElement.__init__(self, base)
        self.points.append('control')
        self.params.append('natural_parametrization')

    def point(self, s):
        if self.natural_parametrization:
            s = self._rescaler(s, s)
        return QuadraticBezier.point(self, s)

    def length(self, **kwargs):
        return self.arclength(1.0)


class SymbolicArc(SymbolicElement, Arc):
    def __init__(self, base):
        self.radius = _imag_to_coord(base.radius)
        self.center = _imag_to_coord(base.center)
        self.theta = base.theta
        self.delta = base.delta
        self.rotation = base.rotation
        self.radius_scale = base.radius_scale
        self.arc = base.arc
        self.sweep = base.sweep
        self.transform = cas.DM.eye(2)
        SymbolicElement.__init__(self, base)
        self.points.extend(['center'])
        # radius scales, but e.g. doesn't rotate; thus, not in points attribute
        self.params.extend(['radius', 'theta', 'delta', 'rotation', 'radius_scale', 'arc', 'sweep', 'transform'])

    def point(self, s):
        if self.natural_parametrization:
            s = self._rescaler(s, s)
        angle = (self.theta + (self.delta * s)) * cas.pi / 180
        cosr = cas.cos(self.rotation * cas.pi / 180)
        sinr = cas.sin(self.rotation * cas.pi / 180)
        radius = self.radius * self.radius_scale

        p = cas.DM(2, 1) if isinstance(s, float) else type(s)(2, 1)
        p[0] = cosr * cas.cos(angle) * radius[0] - sinr * cas.sin(angle) * radius[1]
        p[1] = sinr * cas.cos(angle) * radius[0] + cosr * cas.sin(angle) * radius[1]
        p = self.transform@p + self.center
        return p

    def matrix(self, a, b, c, d, e, f):
        SymbolicElement.matrix(self, a, b, c, d, e, f)
        rot = cas.vertcat(cas.horzcat(a, c), cas.horzcat(b, d))
        self.transform = rot@self.transform

    def length(self, **kwargs):
        return self.arclength(1.0)


class SymbolicMove(SymbolicElement, Move):
    def __init__(self, base):
        SymbolicElement.__init__(self, base)

    def length(self, **kwargs):
        return 0.0


class SymbolicClose(SymbolicElement, Close):
    def __init__(self, base):
        SymbolicElement.__init__(self, base)
