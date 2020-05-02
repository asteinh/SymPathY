import pytest
from tests.mixins import Elements, Transforms
from svg.path import Line, QuadraticBezier
from sympathor.elements import SymbolicLine


class TestLine(Transforms, Elements):
    @pytest.fixture(params=[
        (0 + 0j, 100 + 0j),
        (0 + 0j,  0 + 75j),
        (0 + 0j, 20 + 99j)
    ])
    def element(self, request):
        element_ = Line(*request.param)
        obj = SymbolicLine(element_)
        return {'obj': obj, 'base': element_}

    def test_eq(self, element):
        Elements.test_eq(self, element)
        assert not element['obj'] == QuadraticBezier(0, 1+1j, 2)
        assert not element['obj'] == SymbolicLine(Line(0 + 0j, 10 + 0j))
