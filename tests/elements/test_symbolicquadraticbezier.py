from tests.elements.conftest import EPSILON, SymbolicMixin, CubicBezier, SymbolicQuadraticBezier, QuadraticBezier

import pytest
import casadi as cas
import copy


@pytest.fixture(params=[
    (0 + 0j, 10 + 10j, 20 - 10j),
    (-23.12 + 3.1j, 10.2 + 0j, 0 - 8.5j)
])
def curve(request):
    curve_ = QuadraticBezier(request.param[0], request.param[1], request.param[2])
    return {
        'obj': SymbolicQuadraticBezier(curve_),
        'start': cas.DM([request.param[0].real, request.param[0].imag]),
        'control': cas.DM([request.param[1].real, request.param[1].imag]),
        'end': cas.DM([request.param[2].real, request.param[2].imag]),
        'base': curve_
    }


# TESTS
def test_general(curve):
    # __eq__
    assert not (curve['obj'] == CubicBezier(0, 1+1j, 2, 0))
    curve_ = copy.copy(curve['obj'])
    assert curve_ == curve['obj']


def test_point(curve, sval):
    # test against parent's implementation
    p_ = curve['base'].point(sval)
    assert cas.norm_2(curve['obj'].point(sval) - cas.DM([p_.real, p_.imag])) == 0

    # test natural parametrization
    p_ = curve['base'].point(float(curve['obj']._rescaler(sval, sval)))
    curve['obj']._natural_parametrization = True
    assert cas.norm_2(curve['obj'].point(sval) - cas.DM([p_.real, p_.imag])) == 0


def test_length(curve):
    # test against parent's implementation
    assert cas.fabs(curve['obj'].length() - curve['base'].length()) < EPSILON


def test_arclength(curve, sval):
    assert cas.fabs(curve['obj'].arclength(sval) - SymbolicMixin.arclength(curve['obj'], sval)) < 10*EPSILON


def test_matrix():
    return NotImplemented


@pytest.mark.parametrize('dx', [0, +100, -100, +cas.pi, -cas.pi])
@pytest.mark.parametrize('dy', [0, +100, -100, +cas.pi, -cas.pi])
def test_translate(curve, dx, dy):
    orig = copy.copy(curve['obj'])
    delta = cas.DM([dx, dy])

    curve['obj'].translate(dx, dy)
    assert cas.norm_2(curve['obj'].start - (curve['start'] + delta)) == 0
    assert cas.norm_2(curve['obj'].control - (curve['control'] + delta)) == 0
    assert cas.norm_2(curve['obj'].end - (curve['end'] + delta)) == 0

    curve['obj'].translate(-dx, -dy)
    assert curve['obj'] == orig


@pytest.mark.parametrize('theta', [0, 90, 180, 270])
@pytest.mark.parametrize('x', [0, +cas.pi, -cas.pi])
@pytest.mark.parametrize('y', [0, +cas.pi, -cas.pi])
def test_rotate(curve, theta, x, y):
    curve['obj'].rotate(theta, x, y)
    # TODO assertions


@pytest.mark.parametrize('x', [0, 1, cas.pi])
@pytest.mark.parametrize('y', [0, 1, cas.pi])
def test_scale(curve, x, y):
    orig = copy.copy(curve['obj'])

    curve_ = copy.copy(orig)

    if x == y:
        curve_.scale(x=x, y=None)
    else:
        curve_.scale(x, y)

    assert cas.norm_2(curve_.start - curve['start']*cas.DM([x, y])) == 0
    assert cas.norm_2(curve_.control - curve['control']*cas.DM([x, y])) == 0
    assert cas.norm_2(curve_.end - curve['end']*cas.DM([x, y])) == 0
    if x > 0 and y > 0:
        curve_.scale(1/x, 1/y)
        assert curve_ == orig

    curve_ = copy.copy(orig)
    curve_.scale(-x, y)
    assert cas.norm_2(curve_.start - curve['start']*cas.DM([-x, y])) == 0
    assert cas.norm_2(curve_.control - curve['control']*cas.DM([-x, y])) == 0
    assert cas.norm_2(curve_.end - curve['end']*cas.DM([-x, y])) == 0
    if x > 0 and y > 0:
        curve_.scale(-1/x, 1/y)
        assert curve_ == orig

    curve_ = copy.copy(orig)
    curve_.scale(x, -y)
    assert cas.norm_2(curve_.start - curve['start']*cas.DM([x, -y])) == 0
    assert cas.norm_2(curve_.control - curve['control']*cas.DM([x, -y])) == 0
    assert cas.norm_2(curve_.end - curve['end']*cas.DM([x, -y])) == 0
    if x > 0 and y > 0:
        curve_.scale(1/x, -1/y)
        assert curve_ == orig


def test_skewX():
    return NotImplemented


def test_skewY():
    return NotImplemented
