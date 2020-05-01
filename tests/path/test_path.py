from tests.path.conftest import EPSILON, Line, Path, SymbolicPath  # noqa

# import pytest
# import casadi as cas
import copy


# TESTS
def test_general(path):
    # __eq__
    assert not (path['obj'] == Path(Line(0j, 1j)))
    assert not (path['obj'] == SymbolicPath(Path(Line(0j, 1j))))
    path_ = copy.deepcopy(path['obj'])
    path_._segments[0] = path_._segments[1]
    assert not path_ == path['obj']
    path_ = copy.copy(path['obj'])
    assert path_ == path['obj']
