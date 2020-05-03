import casadi as cas
import copy
from sympathor.elements import SymbolicMixin
import pytest


# DEFINES
EPSILON = 1e-6


class Basics():
    def test_eq(self, element):
        element_ = copy.copy(element['obj'])
        assert element_ == element['obj']

    def test_point(self, element, fx_svals):
        svals = fx_svals

        # test against parent's implementation
        for sval in svals:
            p_ = element['base'].point(sval)
            assert cas.norm_2(element['obj'].point(sval) - cas.DM([p_.real, p_.imag])) < EPSILON

    def test_length(self, element):
        # test against parent's implementation
        assert cas.fabs(element['obj'].length() - element['base'].length()) < EPSILON

    def test_arclength(self, element, fx_svals):
        svals = fx_svals

        for sval in svals:
            assert cas.fabs(element['obj'].arclength(sval) - SymbolicMixin.arclength(element['obj'], sval)) < 10*EPSILON


class Elements(Basics):
    def test_point(self, element, fx_svals):
        svals = fx_svals

        Basics.test_point(self, element, svals)
        for sval in svals:
            # test natural parametrization
            p_ = element['base'].point(float(element['obj']._rescaler(sval, sval)))
            element['obj'].set_natural_parametrization(True)
            assert cas.norm_2(element['obj'].point(sval) - cas.DM([p_.real, p_.imag])) < EPSILON


class Transforms():
    def test_matrix(self, element, fx_theta, fx_dx, fx_dy):
        theta, dx, dy = fx_theta, fx_dx, fx_dy
        T = cas.DM([[+cas.cos(theta / 180 * cas.pi), -cas.sin(theta / 180 * cas.pi)],
                    [+cas.sin(theta / 180 * cas.pi), +cas.cos(theta / 180 * cas.pi)]])
        delta = cas.DM([dx, dy])

        objA = copy.deepcopy(element['obj'])
        objA.matrix(T[0, 0], T[1, 0], T[0, 1], T[1, 1], delta[0], delta[1])
        objB = copy.copy(element['obj'])
        objB.rotate(theta)
        objB.translate(dx, dy)
        assert objA == objB

    def test_translate(self, element, fx_dx, fx_dy, fx_svals):
        dx, dy, svals = fx_dx, fx_dy, fx_svals
        orig = copy.copy(element['obj'])
        delta = cas.DM([dx, dy])

        element['obj'].translate(dx, dy)
        for sval in svals:
            assert cas.norm_2(element['obj'].point(sval) - (orig.point(sval) + delta)) < EPSILON

        element['obj'].translate(-dx, -dy)
        assert element['obj'] == orig

    def test_rotate(self, element, fx_theta, fx_x, fx_y, fx_svals):
        theta, x, y, svals = fx_theta, fx_x, fx_y, fx_svals
        orig = copy.copy(element['obj'])
        delta = cas.DM([x, y])
        T = cas.DM([[+cas.cos(theta / 180 * cas.pi), -cas.sin(theta / 180 * cas.pi)],
                    [+cas.sin(theta / 180 * cas.pi), +cas.cos(theta / 180 * cas.pi)]])

        element['obj'].rotate(theta, x, y)
        for sval in svals:
            p = T@(orig.point(sval) - delta) + delta
            assert cas.norm_2(element['obj'].point(sval) - p) < EPSILON

        element['obj'].rotate(-theta, x, y)
        assert element['obj'] == orig

    def test_scale(self, element, fx_x, fx_y, fx_svals):
        x, y, svals = fx_x, fx_y, fx_svals
        orig = copy.copy(element['obj'])

        element_ = copy.deepcopy(orig)
        if x == y:
            element_.scale(x=x, y=None)
        else:
            element_.scale(x, y)
            for sval in svals:
                assert cas.norm_2(element_.point(sval) - orig.point(sval)*cas.DM([x, y])) < EPSILON
        if x > 0 and y > 0:
            element_.scale(1/x, 1/y)
            assert element_ == orig

        element_ = copy.deepcopy(orig)
        element_.scale(-x, y)
        for sval in svals:
            assert cas.norm_2(element_.point(sval) - orig.point(sval)*cas.DM([-x, y])) < EPSILON
        if x > 0 and y > 0:
            element_.scale(-1/x, 1/y)
            assert element_ == orig

        element_ = copy.deepcopy(orig)
        element_.scale(x, -y)
        for sval in svals:
            assert cas.norm_2(element_.point(sval) - orig.point(sval)*cas.DM([x, -y])) < EPSILON
        if x > 0 and y > 0:
            element_.scale(1/x, -1/y)
            assert element_ == orig

    @pytest.mark.skip(reason="TODO")
    def test_skewx(self, element):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_skewy(self, element):
        pass
