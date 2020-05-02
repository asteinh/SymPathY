import pytest
from tests.mixins import Elements, Transforms
from svg.path import Line, Close
from sympathor.elements import SymbolicClose


class TestClose(Transforms, Elements):
    @pytest.fixture(params=[
        (0 + 0j, 100 + 0j),
        (0 + 0j,  0 + 75j),
        (0 + 0j, 20 + 99j)
    ])
    def element(self, request):
        close_ = Close(*request.param)
        obj = SymbolicClose(close_)
        return {'obj': obj, 'base': close_}

    def test_eq(self, element):
        Elements.test_eq(self, element)
        assert not (element['obj'] == Line(0, 1+1j))
