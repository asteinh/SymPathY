import pytest
from tests.mixins import Elements, Transforms
from svg.path import Line, Move
from sympathor.elements import SymbolicMove


class TestMove(Transforms, Elements):
    @pytest.fixture(params=[
        (100 - 10j),
        (-13.23 + 1000.2j)
    ])
    def element(self, request):
        move_ = Move(request.param)
        obj = SymbolicMove(move_)
        return {'obj': obj, 'base': move_}

    def test_eq(self, element):
        Elements.test_eq(self, element)
        assert not (element['obj'] == Line(0, 1+1j))
