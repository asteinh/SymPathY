from tests.elements.conftest import EPSILON, Line, SymbolicLine, QuadraticBezier

import pytest
import casadi as cas
import copy


@pytest.fixture(params=[
    (0 + 0j, 100 + 0j),
    (0 + 0j,  0 + 75j),
    (0 + 0j, 20 + 99j)
])
def line(request):
    line_ = Line(request.param[0], request.param[1])
    return {
        'obj': SymbolicLine(line_),
        'start': cas.DM([request.param[0].real, request.param[0].imag]),
        'end': cas.DM([request.param[1].real, request.param[1].imag]),
        'base': line_
    }


def rotation_matrix(theta):
    return cas.DM([[+cas.cos(theta / 180 * cas.pi), -cas.sin(theta / 180 * cas.pi)],
                   [+cas.sin(theta / 180 * cas.pi), +cas.cos(theta / 180 * cas.pi)]])


# TESTS
def test_general(line):
    # __eq__
    assert not line['obj'] == QuadraticBezier(0, 1+1j, 2)
    assert not line['obj'] == SymbolicLine(Line(0 + 0j, 10 + 0j))
    line_ = copy.copy(line['obj'])
    assert line_ == line['obj']


def test_point(line, sval):
    # test against parent's implementation
    p_ = line['base'].point(sval)
    assert cas.norm_2(line['obj'].point(sval) - cas.DM([p_.real, p_.imag])) == 0


def test_length(line):
    # test against parent's implementation
    assert cas.fabs(line['obj'].length() - line['base'].length()) < EPSILON


def test_arclength(line, sval):
    assert cas.fabs(line['obj'].arclength(sval) - sval*line['obj'].length()) < EPSILON


@pytest.mark.parametrize('theta', [0, +100, ])  # -100, +cas.pi, -cas.pi])
@pytest.mark.parametrize('dx', [0, +100, ])  # -100, +cas.pi, -cas.pi])
@pytest.mark.parametrize('dy', [0, +100, ])  # -100, +cas.pi, -cas.pi])
def test_matrix(line, theta, dx, dy):
    T = rotation_matrix(theta)
    delta = cas.DM([dx, dy])

    lineA = copy.copy(line['obj'])
    lineA.matrix(T[0, 0], T[1, 0], T[0, 1], T[1, 1], delta[0], delta[1])
    lineB = copy.copy(line['obj'])
    lineB.rotate(theta)
    lineB.translate(dx, dy)
    assert lineA == lineB


@pytest.mark.parametrize('dx', [0, +100, -100, +cas.pi, -cas.pi])
@pytest.mark.parametrize('dy', [0, +100, -100, +cas.pi, -cas.pi])
def test_translate(line, dx, dy):
    orig = copy.copy(line['obj'])
    delta = cas.DM([dx, dy])

    line['obj'].translate(dx, dy)
    assert cas.norm_2(line['obj'].start - (line['start'] + delta)) == 0
    assert cas.norm_2(line['obj'].end - (line['end'] + delta)) == 0

    line['obj'].translate(-dx, -dy)
    assert line['obj'] == orig


@pytest.mark.parametrize('theta', [0, 90, 180, 270])
@pytest.mark.parametrize('x', [0, +cas.pi, -cas.pi])
@pytest.mark.parametrize('y', [0, +cas.pi, -cas.pi])
def test_rotate(line, theta, x, y):
    line['obj'].rotate(theta, x, y)
    # TODO assertions


@pytest.mark.parametrize('x', [0, 1, cas.pi])
@pytest.mark.parametrize('y', [0, 1, cas.pi])
def test_scale(line, x, y):
    orig = copy.copy(line['obj'])

    line_ = copy.copy(orig)
    if x == y:
        line_.scale(x=x, y=None)
    else:
        line_.scale(x, y)
    assert cas.norm_2(line_.start - line['start']*cas.DM([x, y])) == 0
    assert cas.norm_2(line_.end - line['end']*cas.DM([x, y])) == 0
    if x > 0 and y > 0:
        line_.scale(1/x, 1/y)
        assert line_ == orig

    line_ = copy.copy(orig)
    line_.scale(-x, y)
    assert cas.norm_2(line_.start - line['start']*cas.DM([-x, y])) == 0
    assert cas.norm_2(line_.end - line['end']*cas.DM([-x, y])) == 0
    if x > 0 and y > 0:
        line_.scale(-1/x, 1/y)
        assert line_ == orig

    line_ = copy.copy(orig)
    line_.scale(x, -y)
    assert cas.norm_2(line_.start - line['start']*cas.DM([x, -y])) == 0
    assert cas.norm_2(line_.end - line['end']*cas.DM([x, -y])) == 0
    if x > 0 and y > 0:
        line_.scale(1/x, -1/y)
        assert line_ == orig


def test_skewX():
    return NotImplemented


def test_skewY():
    return NotImplemented
