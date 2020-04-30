from svg.path import Line, CubicBezier
from svg.path import QuadraticBezier, Arc  # noqa
from svg.path import Move, Close  # noqa

from sympathor.elements import SymbolicLine, SymbolicCubicBezier
from sympathor.elements import SymbolicQuadraticBezier, SymbolicArc  # noqa
from sympathor.elements import SymbolicMove, SymbolicClose  # noqa

import pytest
import casadi as cas
import copy


@pytest.fixture(params=[0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
def sval(request, scope='module', autouse=True):
    return request.param


class TestLine():
    @pytest.fixture(params=[
        (0 + 0j, 100 + 0j),
        (0 + 0j,  0 + 75j),
        (0 + 0j, 20 + 99j)
    ])
    def line(self, request, scope='class', autouse=True):
        line_ = Line(request.param[0], request.param[1])
        return {
            'obj': SymbolicLine(line_),
            'start': cas.DM([request.param[0].real, request.param[0].imag]),
            'end': cas.DM([request.param[1].real, request.param[1].imag]),
            'base': line_
        }

    # test functions
    def test_point(self, line, sval):
        # test against parent's implementation
        p_ = line['base'].point(sval)
        assert cas.norm_2(line['obj'].point(sval) - cas.DM([p_.real, p_.imag])) == 0

    def test_length(self, line):
        # test against parent's implementation
        assert line['obj'].length() == line['base'].length()

    def test_arclength(self, line, sval):
        assert line['obj'].arclength(sval) - sval*line['obj'].length() < line['obj']._eps

    def test_matrix(self):
        return NotImplemented

    @pytest.mark.parametrize('dx', [0, +100, -100, +cas.pi, -cas.pi])
    @pytest.mark.parametrize('dy', [0, +100, -100, +cas.pi, -cas.pi])
    def test_translate(self, line, dx, dy):
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
    def test_rotate(self, line, theta, x, y):
        line['obj'].rotate(theta, x, y)
        # TODO

    @pytest.mark.parametrize('x', [0, 1, cas.pi])
    @pytest.mark.parametrize('y', [0, 1, cas.pi])
    def test_scale(self, line, x, y):
        orig = copy.copy(line['obj'])

        line_ = copy.copy(orig)
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

    def test_skewX(self):
        return NotImplemented

    def test_skewY(self):
        return NotImplemented


class TestCubicBezier():
    @pytest.fixture(params=[
        (0 + 0j, 10 + 10j, 20 + 10j, 30 + 0j),
    ])
    def curve(self, request, scope='class', autouse=True):
        curve_ = CubicBezier(request.param[0], request.param[1], request.param[2], request.param[3])
        return {
            'obj': SymbolicCubicBezier(curve_),
            'start': cas.DM([request.param[0].real, request.param[0].imag]),
            'control1': cas.DM([request.param[1].real, request.param[1].imag]),
            'control2': cas.DM([request.param[2].real, request.param[2].imag]),
            'end': cas.DM([request.param[3].real, request.param[3].imag]),
            'base': curve_
        }

    def test_point(self, curve, sval):
        # test against parent's implementation
        p_ = curve['base'].point(sval)
        assert cas.norm_2(curve['obj'].point(sval) - cas.DM([p_.real, p_.imag])) == 0

    def test_length(self, curve):
        # test against parent's implementation
        assert curve['obj'].length() == curve['base'].length()

    def test_arclength(self, curve, sval):
        assert curve['obj'].arclength(sval) - sval*curve['obj'].length() < curve['obj']._eps

    def test_matrix(self):
        return NotImplemented

    @pytest.mark.parametrize('dx', [0, +100, -100, +cas.pi, -cas.pi])
    @pytest.mark.parametrize('dy', [0, +100, -100, +cas.pi, -cas.pi])
    def test_translate(self, curve, dx, dy):
        pass

    @pytest.mark.parametrize('theta', [0, 90, 180, 270])
    @pytest.mark.parametrize('x', [0, +cas.pi, -cas.pi])
    @pytest.mark.parametrize('y', [0, +cas.pi, -cas.pi])
    def test_rotate(self, curve, theta, x, y):
        pass

    @pytest.mark.parametrize('x', [0, 1, cas.pi])
    @pytest.mark.parametrize('y', [0, 1, cas.pi])
    def test_scale(self, curve, x, y):
        pass

    def test_skewX(self):
        return NotImplemented

    def test_skewY(self):
        return NotImplemented
