import pytest
from tests.mixins import Basics, Transforms, EPSILON
from svg.path import Path, Line, Arc, Close, QuadraticBezier, CubicBezier
from sympathor.path import SymbolicPath
import casadi as cas
import copy


class TestPath(Transforms, Basics):
    @pytest.fixture(params=[
        (  # circle
            Arc(0j, 100 + 100j, 0, 0, 0, 200 + 0j),
            Arc(200 + 0j, 100 + 100j, 0, 0, 0, 0j)
        ),
        (  # some elements
            Line(600 + 350j, 650 + 325j),
            Arc(650 + 325j, 25 + 25j, -30, 0, 1, 700 + 300j),
            CubicBezier(700 + 300j, 800 + 400j, 750 + 200j, 600 + 100j),
            QuadraticBezier(600 + 100j, 500 + 400j, 600 + 350j),
            Close(600 + 350j, 600 + 350j)
        )
    ])
    def element(self, request):
        base = Path(*request.param)
        obj = SymbolicPath(base)
        return {'obj': obj, 'base': base}

    # BASICS
    def test_eq(self, element):
        Basics.test_eq(self, element)
        assert not (element['obj'] == Path(Line(0j, 1j)))
        assert not (element['obj'] == SymbolicPath(Path(Line(0j, 1j))))
        element_ = copy.deepcopy(element['obj'])
        element_._segments[0] = element_._segments[1]
        assert not element_ == element['obj']

    def test_point(self, element, sval):
        Basics.test_point(self, element, sval)
        assert type(element['obj'].point()) == cas.Function

    # TRANSFORMS
    @pytest.mark.skip(reason="Unclear how to handle Arc-attribute 'rotation' when using matrix transformation.")
    def test_matrix(self, element, theta, dx, dy):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_translate(self):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_rotate(self):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_scale(self):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_skewx(self):
        pass

    @pytest.mark.skip(reason="TODO")
    def test_skewy(self):
        pass

    # DIFFERENTIAL GEOMETRY
    def test_tangent(self, element, sval):
        assert type(element['obj'].tangent()) == cas.Function

        # check if the tangent is an appropriate linearization
        if sval < 1.0:
            sval_ = sval + EPSILON
        else:
            sval = 1.0 - EPSILON
            sval_ = 1.0
        P = element['obj'].point(sval)
        t = element['obj'].tangent(sval)
        delta = element['obj'].arclength(sval_) - element['obj'].arclength(sval)
        T_ = P + delta*t
        P_ = element['obj'].point(sval_)
        assert cas.norm_2(T_ - P_) <= cas.norm_2(P_ - P)

        # unit length
        assert 1 - cas.norm_2(t) < EPSILON

    def test_normal(self, element, sval):
        assert type(element['obj'].normal()) == cas.Function

        # normal to tangent
        t = element['obj'].tangent(sval)
        n = element['obj'].normal(sval)
        assert cas.fabs(cas.dot(t, n)) < EPSILON

        # unit length
        assert 1 - cas.norm_2(n) < EPSILON

    def test_curvature(self, element, sval):
        assert type(element['obj'].curvature()) == cas.Function

        # check if approximation is close
        if sval < 1.0:
            sval_ = sval + EPSILON
        else:
            sval = 1.0 - EPSILON
            sval_ = 1.0
        dp_ds = (element['obj'].point(sval_) - element['obj'].point(sval)) / EPSILON
        dt_ds = (element['obj'].tangent(sval_) - element['obj'].tangent(sval)) / EPSILON
        c = element['obj'].curvature(sval_)
        assert cas.fabs(cas.norm_2(dt_ds) / cas.norm_2(dp_ds) - c) < EPSILON
