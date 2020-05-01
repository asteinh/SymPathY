from svg.path import Path, Line, Arc, QuadraticBezier, CubicBezier

from sympathor.path import SymbolicPath  # noqa

import pytest

# DEFINES
EPSILON = 1e-6

# PYTEST FIXTURES
@pytest.fixture(params=[0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
def sval(request, scope='module'):
    return request.param


@pytest.fixture(params=[
    (  # circle
        Arc(0j, 100 + 100j, 0, 0, 0, 200 + 0j),
        Arc(200 + 0j, 100 + 100j, 0, 0, 0, 0j)
    ),
    (  # some elements
        Line(600 + 350j, 650 + 325j),
        Arc(650 + 325j, 25 + 25j, -30, 0, 1, 700 + 300j),
        CubicBezier(700 + 300j, 800 + 400j, 750 + 200j, 600 + 100j),
        QuadraticBezier(600 + 100j, 600, 600 + 300j)
    )
])
def path(request):
    base = Path(*request.param)
    obj = SymbolicPath(base)
    return {
        'base': base,
        'obj': obj
    }
