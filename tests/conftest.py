import casadi as cas
import pytest

# PYTEST FIXTURES
@pytest.fixture(scope='module')
def fx_svals(request):
    return [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]


@pytest.fixture(params=[0, +100, -100, +cas.pi, -cas.pi], scope='module')
def fx_theta(request):
    return request.param


@pytest.fixture(params=[0, +cas.pi, -cas.pi], scope='module')
def fx_x(request):
    return request.param


@pytest.fixture(params=[0, +cas.pi, -cas.pi], scope='module')
def fx_y(request):
    return request.param


@pytest.fixture(params=[0, +cas.pi, -cas.pi], scope='module')
def fx_dx(request):
    return request.param


@pytest.fixture(params=[0, +cas.pi, -cas.pi], scope='module')
def fx_dy(request):
    return request.param


@pytest.fixture
def element(request):
    raise NotImplementedError
