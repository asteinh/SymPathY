import pytest
from tests.mixins import Elements, Transforms
from svg.path import QuadraticBezier, CubicBezier
from sympathor.elements import SymbolicCubicBezier


class TestCubicBezier(Transforms, Elements):
    @pytest.fixture(params=[
        (0 + 0j, 10 + 10j, 20 - 10j, 30 + 0j),
        (-23.12 + 3.1j, 10.2 + 0j, 0 - 8.5j, -40 + -5.1j)
    ])
    def element(self, request):
        element_ = CubicBezier(*request.param)
        obj = SymbolicCubicBezier(element_)
        return {'obj': obj, 'base': element_}

    def test_eq(self, element):
        Elements.test_eq(self, element)
        assert not (element['obj'] == QuadraticBezier(0, 1+1j, 2))
