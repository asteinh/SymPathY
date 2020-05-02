import pytest
from tests.mixins import Elements, Transforms
from svg.path import QuadraticBezier, CubicBezier
from sympathor.elements import SymbolicQuadraticBezier


class TestQuadraticBezier(Transforms, Elements):
    @pytest.fixture(params=[
        (0 + 0j, 10 + 10j, 20 - 10j),
        (-23.12 + 3.1j, 10.2 + 0j, 0 - 8.5j)
    ])
    def element(self, request):
        curve_ = QuadraticBezier(*request.param)
        obj = SymbolicQuadraticBezier(curve_)
        return {'obj': obj, 'base': curve_}

    def test_eq(self, element):
        Elements.test_eq(self, element)
        assert not (element['obj'] == CubicBezier(0, 1+1j, 2, 0))
