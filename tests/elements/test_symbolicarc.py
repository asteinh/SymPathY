from tests.elements.conftest import EPSILON, SymbolicMixin, Arc, SymbolicArc, QuadraticBezier

import pytest
import casadi as cas
import copy


@pytest.fixture(params=[
    (0j, 100 + 50j, 0, 0, 0, 100 + 50j),
])
def arc(request):
    arc_ = Arc(*request.param)
    obj = SymbolicArc(arc_)
    return {
        'base': arc_,
        'obj': obj,
        'start': obj.start,
        'radius': obj.radius,
        'center': obj.center,
        'end': obj.end
    }


# TESTS
def test_general(arc):
    # __eq__
    assert not (arc['obj'] == QuadraticBezier(0, 1+1j, 2))
    arc_ = copy.copy(arc['obj'])
    assert arc_ == arc['obj']


def test_point(arc, sval):
    # test against parent's implementation
    p_ = arc['base'].point(sval)
    assert cas.norm_2(arc['obj'].point(sval) - cas.DM([p_.real, p_.imag])) < EPSILON

    # test natural parametrization
    p_ = arc['base'].point(float(arc['obj']._rescaler(sval, sval)))
    arc['obj'].set_natural_parametrization(True)
    assert cas.norm_2(arc['obj'].point(sval) - cas.DM([p_.real, p_.imag])) < EPSILON


def test_length(arc):
    # test against parent's implementation
    assert cas.fabs(arc['obj'].length() - arc['base'].length()) < EPSILON


def test_arclength(arc, sval):
    assert cas.fabs(arc['obj'].arclength(sval) - SymbolicMixin.arclength(arc['obj'], sval)) < 10*EPSILON


def test_matrix():
    return NotImplemented


@pytest.mark.parametrize('dx', [0, +100, -100, +cas.pi, -cas.pi])
@pytest.mark.parametrize('dy', [0, +100, -100, +cas.pi, -cas.pi])
def test_translate(arc, dx, dy):
    orig = copy.copy(arc['obj'])
    delta = cas.DM([dx, dy])

    arc['obj'].translate(dx, dy)
    assert cas.norm_2(arc['obj'].start - (arc['start'] + delta)) == 0
    assert cas.norm_2(arc['obj'].center - (arc['center'] + delta)) == 0
    assert cas.norm_2(arc['obj'].end - (arc['end'] + delta)) == 0

    arc['obj'].translate(-dx, -dy)
    assert arc['obj'] == orig


@pytest.mark.parametrize('theta', [0, 90, 180, 270])
@pytest.mark.parametrize('x', [0, +cas.pi, -cas.pi])
@pytest.mark.parametrize('y', [0, +cas.pi, -cas.pi])
def test_rotate(arc, theta, x, y):
    arc['obj'].rotate(theta, x, y)
    # TODO assertions


@pytest.mark.parametrize('x', [0, 1, cas.pi])
@pytest.mark.parametrize('y', [0, 1, cas.pi])
def test_scale(arc, x, y):
    orig = copy.copy(arc['obj'])

    arc_ = copy.copy(orig)

    if x == y:
        arc_.scale(x=x, y=None)
    else:
        arc_.scale(x, y)

    assert cas.norm_2(arc_.start - arc['start']*cas.DM([x, y])) == 0
    assert cas.norm_2(arc_.radius - arc['radius']*cas.DM([x, y])) == 0
    assert cas.norm_2(arc_.center - arc['center']*cas.DM([x, y])) == 0
    assert cas.norm_2(arc_.end - arc['end']*cas.DM([x, y])) == 0
    if x > 0 and y > 0:
        arc_.scale(1/x, 1/y)
        assert arc_ == orig

    arc_ = copy.copy(orig)
    arc_.scale(-x, y)
    assert cas.norm_2(arc_.start - arc['start']*cas.DM([-x, y])) == 0
    assert cas.norm_2(arc_.radius - arc['radius']*cas.DM([-x, y])) == 0
    assert cas.norm_2(arc_.center - arc['center']*cas.DM([-x, y])) == 0
    assert cas.norm_2(arc_.end - arc['end']*cas.DM([-x, y])) == 0
    if x > 0 and y > 0:
        arc_.scale(-1/x, 1/y)
        assert arc_ == orig

    arc_ = copy.copy(orig)
    arc_.scale(x, -y)
    assert cas.norm_2(arc_.start - arc['start']*cas.DM([x, -y])) == 0
    assert cas.norm_2(arc_.radius - arc['radius']*cas.DM([x, -y])) == 0
    assert cas.norm_2(arc_.center - arc['center']*cas.DM([x, -y])) == 0
    assert cas.norm_2(arc_.end - arc['end']*cas.DM([x, -y])) == 0
    if x > 0 and y > 0:
        arc_.scale(1/x, -1/y)
        assert arc_ == orig


def test_skewX():
    return NotImplemented


def test_skewY():
    return NotImplemented
