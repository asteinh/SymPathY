import pytest
from tests.mixins import Elements, Transforms
from svg.path import QuadraticBezier, Arc
from sympathor.elements import SymbolicArc


class TestArc(Transforms, Elements):
    @pytest.fixture(params=[
        (0j, 100 + 50j, 0, 0, 0, 100 + 50j),
    ])
    def element(self, request):
        arc_ = Arc(*request.param)
        obj = SymbolicArc(arc_)
        return {'obj': obj, 'base': arc_}

    def test_eq(self, element):
        Elements.test_eq(self, element)
        assert not (element['obj'] == QuadraticBezier(0, 1+1j, 2))

    @pytest.mark.skip(reason="Unclear how to handle attribute 'rotation' when using matrix transformation.")
    def test_matrix(self, element, theta, dx, dy):
        pass
