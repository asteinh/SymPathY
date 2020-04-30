from tests.elements.conftest import EPSILON, Line, Move, SymbolicMove

import pytest
import casadi as cas
import copy


@pytest.fixture(params=[
    (100 - 10j),
    (-13.23 + 1000.2j)
])
def move(request):
    move_ = Move(request.param)
    return {
        'obj': SymbolicMove(move_),
        'start': cas.DM([request.param.real, request.param.imag]),
        'end': cas.DM([request.param.real, request.param.imag]),
        'base': move_
    }


# TESTS
def test_general(move):
    # __eq__
    assert not (move['obj'] == Line(0, 1+1j))
    move_ = copy.copy(move['obj'])
    assert move_ == move['obj']


def test_length(move):
    # test against parent's implementation
    assert cas.fabs(move['obj'].length() - move['base'].length()) < EPSILON
