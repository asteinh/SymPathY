import casadi as cas
import pytest

# PYTEST FIXTURES
@pytest.fixture(params=[0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0], scope='module')
def sval(request):
    return request.param


@pytest.fixture(scope='module')
def sval_grid(request):
    return [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]


@pytest.fixture(params=[0, +100, -100, +cas.pi, -cas.pi], scope='module')
def theta(request):
    return request.param


@pytest.fixture(params=[0, +cas.pi, -cas.pi], scope='module')
def x(request):
    return request.param


@pytest.fixture(params=[0, +cas.pi, -cas.pi], scope='module')
def y(request):
    return request.param


@pytest.fixture(params=[0, +cas.pi, -cas.pi], scope='module')
def dx(request):
    return request.param


@pytest.fixture(params=[0, +cas.pi, -cas.pi], scope='module')
def dy(request):
    return request.param


@pytest.fixture
def element(request):
    raise NotImplementedError
