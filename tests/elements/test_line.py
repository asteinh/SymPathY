from svg.path import Line
from sympathor.elements import SymbolicLine

import unittest
from nose2.tools import params


class TestLine(unittest.TestCase):
    @params(
        (Line(0 + 0j, 100 + 0j), 100.),
        (Line(0 + 0j, 0 + 75j), 75.),
        (Line(0 + 0j, 20 + 99j), 101.)
    )
    def test_length(self, line, exp_length):
        sline = SymbolicLine(line)
        self.assertAlmostEqual(sline.length(), exp_length)

        # translate
        sline.translate(500, 200)
        self.assertAlmostEqual(sline.length(), exp_length)
        sline.translate(-200)
        self.assertAlmostEqual(sline.length(), exp_length)

        # rotate
        sline.rotate(-193)
        self.assertAlmostEqual(sline.length(), exp_length)
        sline.rotate(33, -250, -150)
        self.assertAlmostEqual(sline.length(), exp_length)

        # scale
        sline.scale(1.5)
        self.assertAlmostEqual(sline.length(), 1.5*exp_length)
        sline.scale(-3)
        self.assertAlmostEqual(sline.length(), 4.5*exp_length)
