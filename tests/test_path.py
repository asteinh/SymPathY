import pytest
from tests.mixins import Basics, Transforms, EPSILON
from svg.path import Path, Line, Arc, Close, QuadraticBezier, CubicBezier  # noqa
from sympathor.path import SymbolicPath
import casadi as cas
import copy


class TestPath(Transforms, Basics):
    @pytest.fixture(params=[
        # (  # circle
        #     Arc(0j, 100 + 100j, 0, 0, 0, 200 + 0j),
        #     Arc(200 + 0j, 100 + 100j, 0, 0, 0, 0j)
        # ),
        (  # some elements
            Line(600 + 350j, 650 + 325j),
            CubicBezier(650 + 325j, 800 + 400j, 750 + 200j, 600 + 100j),
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

    def test_point(self, element, fx_svals):
        svals = fx_svals

        Basics.test_point(self, element, svals)
        for sval in svals:
            assert type(element['obj'].point()) == cas.Function

    # DIFFERENTIAL GEOMETRY
    def test_tangent(self, element, fx_svals):
        svals = fx_svals
        assert type(element['obj'].tangent()) == cas.Function

        for sval in svals:
            # check if the tangent is an appropriate linearization
            if sval < 1.0:
                sval_ = sval + EPSILON
            else:
                sval = 1.0 - EPSILON
                sval_ = 1.0
            P = element['obj'].point(sval)
            t = element['obj'].tangent(sval)
            T_ = P + EPSILON*t
            P_ = element['obj'].point(sval_)
            assert cas.norm_2(T_ - P_) <= cas.norm_2(P_ - P)
            # unit length
            assert 1 - cas.norm_2(t) < EPSILON

    def test_normal(self, element, fx_svals):
        svals = fx_svals
        assert type(element['obj'].normal()) == cas.Function

        for sval in svals:
            # normal to tangent
            t = element['obj'].tangent(sval)
            n = element['obj'].normal(sval)
            assert cas.fabs(cas.dot(t, n)) < EPSILON
            # unit length
            assert 1 - cas.norm_2(n) < EPSILON

    def test_curvature(self, element, fx_svals):
        svals = fx_svals
        assert type(element['obj'].curvature()) == cas.Function

        for sval in svals:
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
