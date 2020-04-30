from svg.path import Line, CubicBezier, QuadraticBezier, Arc, Move, Close  # noqa

from sympathor.elements import SymbolicMixin, SymbolicElement  # noqa
from sympathor.elements import SymbolicLine, SymbolicCubicBezier  # noqa
from sympathor.elements import SymbolicQuadraticBezier, SymbolicArc  # noqa
from sympathor.elements import SymbolicMove, SymbolicClose  # noqa

import pytest

# DEFINES
EPSILON = 1e-6

# PYTEST FIXTURES
@pytest.fixture(params=[0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
def sval(request, scope='module'):
    return request.param
