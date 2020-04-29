from svg.path import Line, CubicBezier, QuadraticBezier, Arc, Move, Close
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
        self._s = cas.MX.sym('s')
        self._expr = cas.MX.nan(2, 1)

    def arclength(self, s):
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
        self.start = cas.DM([base.start.real, base.start.imag])
        self.end = cas.DM([base.end.real, base.end.imag])
        if expr_from:
            self._expr = expr_from(self, self._s)
        else:
            self._expr = self.point(self._s)

        self._natural_parametrization = False
        self._rescaler = self._setup_rescaler()

    def arclength(self, s):
        # approximation of arc length for elements
        fcn = cas.Function('fcn', [self._s], [cas.norm_2(cas.jacobian(self._expr, self._s))])
        return quadrature(fcn, 0.0, s)

    def _setup_rescaler(self):
        # find a point where arc length == s * length
        s_noli = cas.MX.sym('s_noli')
        fcn = cas.Function('fcn', [self._s, s_noli], [self.arclength(self._s) - s_noli*self.length()])
        return cas.rootfinder('r', 'newton', fcn)

    def length(self, **kwargs):
        return float(self.arclength(1.0))

    def matrix(self, a, b, c, d, e, f):
        rot = cas.DM([[a, c], [b, d]])
        delta = cas.DM([e, f])
        self.start = rot@self.start + delta
        self.end = rot@self.end + delta

    def translate(self, dx, dy=0):
        delta = cas.DM([dx, dy])
        self.start += delta
        self.end += delta

    def _pre_rotate(self, theta, x, y):
        self.translate(dx=-x, dy=-y)
        return cas.DM([[+cas.cos(theta / 180 * cas.pi), -cas.sin(theta / 180 * cas.pi)],
                       [+cas.sin(theta / 180 * cas.pi), +cas.cos(theta / 180 * cas.pi)]])

    def _post_rotate(self, x, y):
        self.translate(dx=x, dy=y)

    def rotate(self, theta, x=0, y=0):
        rot = self._pre_rotate(theta, x, y)
        self.start = rot@self.start
        self.end = rot@self.end
        self._post_rotate(x, y)

    def scale(self, x, y=None):
        if y is None:
            y = x
        scaler = cas.DM([x, y])
        self.start *= scaler
        self.end *= scaler

    def skewX(self, theta):
        raise NotImplementedError  # TODO

    def skewY(self, theta):
        raise NotImplementedError  # TODO


class SymbolicLine(SymbolicElement, Line):
    def __init__(self, base):
        SymbolicElement.__init__(self, base)

    def length(self, **kwargs):
        return float(cas.norm_2(self.end-self.start))


class SymbolicCubicBezier(SymbolicElement, CubicBezier):
    def __init__(self, base):
        self.control1 = cas.DM([base.control1.real, base.control1.imag])
        self.control2 = cas.DM([base.control2.real, base.control2.imag])
        SymbolicElement.__init__(self, base, expr_from=CubicBezier.point)

    def point(self, s):
        if self._natural_parametrization:
            return CubicBezier.point(self, self._rescaler(s, s))
        else:
            return CubicBezier.point(self, s)

    def translate(self, dx, dy=0):
        delta = cas.DM([dx, dy])
        self.start += delta
        self.control1 += delta
        self.control2 += delta
        self.end += delta

    def rotate(self, theta, x=0, y=0):
        rot = self._pre_rotate(theta, x, y)
        self.start = rot@self.start
        self.control1 = rot@self.control1
        self.control2 = rot@self.control2
        self.end = rot@self.end
        self._post_rotate(x, y)


class SymbolicQuadraticBezier(SymbolicElement, QuadraticBezier):
    def __init__(self, base):
        self.control = cas.DM([base.control.real, base.control.imag])
        SymbolicElement.__init__(self, base, expr_from=QuadraticBezier.point)

    def point(self, s):
        if self._natural_parametrization:
            return QuadraticBezier.point(self, self._rescaler(s, s))
        else:
            return QuadraticBezier.point(self, s)

    def translate(self, dx, dy=0):
        delta = cas.DM([dx, dy])
        self.start += delta
        self.control += delta
        self.end += delta

    def rotate(self, theta, x=0, y=0):
        rot = self._pre_rotate(theta, x, y)
        self.start = rot@self.start
        self.control = rot@self.control
        self.end = rot@self.end
        self._post_rotate(x, y)


class SymbolicArc(SymbolicElement, Arc):
    def __init__(self, base):
        self.start = cas.DM([base.start.real, base.start.imag])
        self.radius = cas.DM([base.radius.real, base.radius.imag])
        self.center = cas.DM([base.center.real, base.center.imag])
        self.end = cas.DM([base.end.real, base.end.imag])
        self.theta = base.theta
        self.delta = base.delta
        self.rotation = base.rotation
        self.radius_scale = base.radius_scale
        SymbolicElement.__init__(self, base)

    def point(self, s):
        if cas.norm_2(self.start-self.end) < 1e-16:
            return self.start

        if self.radius[0] == 0 or self.radius[1] == 0:
            return self.start + (self.end - self.start) * s

        angle = (self.theta + (self.delta * s)) * cas.pi / 180
        cosr = cas.cos(self.rotation * cas.pi / 180)
        sinr = cas.sin(self.rotation * cas.pi / 180)
        radius = self.radius * self.radius_scale

        p = cas.MX(2, 1)
        p[0] = cosr * cas.cos(angle) * radius[0] - sinr * cas.sin(angle) * radius[1] + self.center[0]
        p[1] = sinr * cas.cos(angle) * radius[0] + cosr * cas.sin(angle) * radius[1] + self.center[1]
        return p

    def translate(self, dx, dy=0):
        delta = cas.DM([dx, dy])
        self.start += delta
        self.center += delta
        self.end += delta

    def rotate(self, theta, x=0, y=0):
        rot = self._pre_rotate(theta, x, y)
        self.start = rot@self.start
        self.center = rot@self.center
        self.rotation = theta
        self.end = rot@self.end
        self._post_rotate(x, y)


class SymbolicMove(SymbolicElement, Move):
    def __init__(self, base):
        SymbolicElement.__init__(self, base)

    def length(self, **kwargs):
        return 0.0


class SymbolicClose(SymbolicElement, Close):
    def __init__(self, base):
        SymbolicElement.__init__(self, base)

    def length(self, **kwargs):
        return float(cas.norm_2(self.end-self.start))
