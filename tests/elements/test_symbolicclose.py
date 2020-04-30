from tests.elements.conftest import EPSILON, Close, Line, SymbolicClose

import pytest
import casadi as cas
import copy


@pytest.fixture(params=[
    (0 + 0j, 100 + 0j),
    (0 + 0j,  0 + 75j),
    (0 + 0j, 20 + 99j)
])
def close(request):
    close_ = Close(request.param[0], request.param[1])
    return {
        'obj': SymbolicClose(close_),
        'start': cas.DM([request.param[0].real, request.param[0].imag]),
        'end': cas.DM([request.param[1].real, request.param[1].imag]),
        'base': close_
    }


# TESTS
def test_general(close):
    # __eq__
    assert not (close['obj'] == Line(0, 1+1j))
    close_ = copy.copy(close['obj'])
    assert close_ == close['obj']


def test_length(close):
    # test against parent's implementation
    assert cas.fabs(close['obj'].length() - close['base'].length()) < EPSILON
