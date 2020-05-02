import casadi as cas
import copy
from sympathor.elements import SymbolicMixin

# DEFINES
EPSILON = 1e-6


class Basics():
    def test_eq(self, element):
        element_ = copy.copy(element['obj'])
        assert element_ == element['obj']

    def test_point(self, element, sval):
        # test against parent's implementation
        p_ = element['base'].point(sval)
        assert cas.norm_2(element['obj'].point(sval) - cas.DM([p_.real, p_.imag])) < EPSILON

    def test_length(self, element):
        # test against parent's implementation
        assert cas.fabs(element['obj'].length() - element['base'].length()) < EPSILON

    def test_arclength(self, element, sval):
        assert cas.fabs(element['obj'].arclength(sval) - SymbolicMixin.arclength(element['obj'], sval)) < 10*EPSILON


class Elements(Basics):
    def test_point(self, element, sval):
        Basics.test_point(self, element, sval)
        # test natural parametrization
        p_ = element['base'].point(float(element['obj']._rescaler(sval, sval)))
        element['obj'].set_natural_parametrization(True)
        assert cas.norm_2(element['obj'].point(sval) - cas.DM([p_.real, p_.imag])) < EPSILON


class Transforms():
    def test_matrix(self, element, theta, dx, dy):
        T = cas.DM([[+cas.cos(theta / 180 * cas.pi), -cas.sin(theta / 180 * cas.pi)],
                    [+cas.sin(theta / 180 * cas.pi), +cas.cos(theta / 180 * cas.pi)]])
        delta = cas.DM([dx, dy])

        objA = copy.deepcopy(element['obj'])
        objA.matrix(T[0, 0], T[1, 0], T[0, 1], T[1, 1], delta[0], delta[1])
        objB = copy.copy(element['obj'])
        objB.rotate(theta)
        objB.translate(dx, dy)
        assert objA == objB

    def test_translate(self, element, dx, dy, sval_grid):
        orig = copy.copy(element['obj'])
        delta = cas.DM([dx, dy])

        element['obj'].translate(dx, dy)
        for s in sval_grid:
            assert cas.norm_2(element['obj'].point(s) - (orig.point(s) + delta)) < EPSILON

        element['obj'].translate(-dx, -dy)
        assert element['obj'] == orig

    def test_rotate(self, element, theta, x, y):
        pass

    def test_scale(self, element, x, y, sval_grid):
        orig = copy.deepcopy(element['obj'])

        element_ = copy.deepcopy(orig)
        if x == y:
            element_.scale(x=x, y=None)
        else:
            element_.scale(x, y)
            for s in sval_grid:
                assert cas.norm_2(element_.point(s) - orig.point(s)*cas.DM([x, y])) < EPSILON
        if x > 0 and y > 0:
            element_.scale(1/x, 1/y)
            assert element_ == orig

        element_ = copy.deepcopy(orig)
        element_.scale(-x, y)
        for s in sval_grid:
            assert cas.norm_2(element_.point(s) - orig.point(s)*cas.DM([-x, y])) < EPSILON
        if x > 0 and y > 0:
            element_.scale(-1/x, 1/y)
            assert element_ == orig

        element_ = copy.deepcopy(orig)
        element_.scale(x, -y)
        for s in sval_grid:
            assert cas.norm_2(element_.point(s) - orig.point(s)*cas.DM([x, -y])) < EPSILON
        if x > 0 and y > 0:
            element_.scale(1/x, -1/y)
            assert element_ == orig

    def test_skewx(self, element):
        pass

    def test_skewy(self, element):
        pass
