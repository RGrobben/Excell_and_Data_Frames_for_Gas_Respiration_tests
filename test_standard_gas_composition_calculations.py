import math
import unittest
from hypothesis import given
import hypothesis.strategies as st

import pandas as pd

from data_frame_calculations import MolPlainFormula


class TestMolPlainFormula(unittest.TestCase):

    def test_mg_bs_in_mol_plain_formula_1(self):
        # Test case 1
        pressure_sample_before = 1020.5
        Rgas = 8314.5
        exp_temperature = 293.15
        volume_headspace = 0.961
        expected_result = 0.04023558874986516
        result = MolPlainFormula.mg_bs_in_mol_plain_formula(pressure_sample_before, Rgas, exp_temperature, volume_headspace)
        self.assertAlmostEqual(result, expected_result, delta=0.0001)


    def test_mg_bs_in_mol_plain_formula_2(self):
        # Test case 2
        pressure_sample_before = 40
        Rgas = 8314.5
        exp_temperature = 293.15
        volume_headspace = 0.961
        expected_result = 0.0015770931406120592
        result = MolPlainFormula.mg_bs_in_mol_plain_formula(pressure_sample_before, Rgas, exp_temperature, volume_headspace)
        self.assertAlmostEqual(result, expected_result, delta=0.0001)

if __name__ == '__main__':
    unittest.main()
