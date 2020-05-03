import pytest
from tests.mixins import Elements, Transforms
from svg.path import Line, QuadraticBezier, CubicBezier, Arc, Move, Close
from sympathor.elements import SymbolicLine, SymbolicQuadraticBezier, SymbolicCubicBezier
from sympathor.elements import SymbolicArc, SymbolicMove, SymbolicClose


class TestLine(Transforms, Elements):
    @pytest.fixture(params=[
        (0 + 0j, 100 + 0j),
        (0 + 0j,  0 + 75j),
        (0 + 0j, 20 + 99j)
    ])
    def element(self, request):
        element_ = Line(*request.param)
        obj = SymbolicLine(element_)
        return {'obj': obj, 'base': element_}

    def test_eq(self, element):
        Elements.test_eq(self, element)
        assert not element['obj'] == QuadraticBezier(0, 1+1j, 2)
        assert not element['obj'] == SymbolicLine(Line(0 + 0j, 10 + 0j))


class TestCubicBezier(Transforms, Elements):
    @pytest.fixture(params=[
        (0 + 0j, 10 + 10j, 20 - 10j, 30 + 0j),
        (-23.12 + 3.1j, 10.2 + 0j, 0 - 8.5j, -40 + -5.1j)
    ])
    def element(self, request):
        element_ = CubicBezier(*request.param)
        obj = SymbolicCubicBezier(element_)
        return {'obj': obj, 'base': element_}

    def test_eq(self, element):
        Elements.test_eq(self, element)
        assert not (element['obj'] == QuadraticBezier(0, 1+1j, 2))


class TestQuadraticBezier(Transforms, Elements):
    @pytest.fixture(params=[
        (0 + 0j, 10 + 10j, 20 - 10j),
        (-23.12 + 3.1j, 10.2 + 0j, 0 - 8.5j)
    ])
    def element(self, request):
        curve_ = QuadraticBezier(*request.param)
        obj = SymbolicQuadraticBezier(curve_)
        return {'obj': obj, 'base': curve_}

    def test_eq(self, element):
        Elements.test_eq(self, element)
        assert not (element['obj'] == CubicBezier(0, 1+1j, 2, 0))


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
