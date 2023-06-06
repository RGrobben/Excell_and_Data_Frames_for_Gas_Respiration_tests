import unittest

import numpy as np
import pandas as pd

from standard_gas_composition_calculations import MolesProduced, CumulativeProductionGasPhase, GasComposition, \
    MolGasCompositionCalculations


class GasCompositionTests(unittest.TestCase):

    def test_set_gas_composition(self):
        data_frame = pd.DataFrame(columns=["CH4 [%]", "CO2 [%]", "O2 [%]", "N2 [%]"])
        GasComposition.set_gas_composition(data_frame, 10.0, 20.0, 30.0, 40.0)
        expected_values = [10.0, 20.0, 30.0, 40.0]
        actual_values = data_frame.loc[0, ["CH4 [%]", "CO2 [%]", "O2 [%]", "N2 [%]"]].tolist()
        self.assertEqual(actual_values, expected_values)

    def test_sum_correct_sum(self):
        data_frame = pd.DataFrame({
            "CH4 [%]": [10.0, 20.0, 30.0],
            "CO2 [%]": [30.0, 20.0, 10.0],
            "O2 [%]": [30.0, 40.0, 10.0],
            "N2 [%]": [30.0, 20.0, 50.0]
        })
        GasComposition.sum_correct_sum(data_frame)
        expected_values = [100.0, 100.0, 100.0]
        actual_values = data_frame["Sum-corr [%]"].tolist()
        self.assertEqual(actual_values, expected_values)

        for i in ["CH4", "CO2", "O2", "N2"]:
            expected_values = [100.0] * 3
            actual_values = data_frame[f"{i}-corr [%]"].tolist()
            self.assertEqual(actual_values, expected_values)


class MolGasCompositionCalculationsTests(unittest.TestCase):

    def setUp(self):
        self.data_frame = pd.DataFrame({
            "P sample before gc [hPa]": [1000, 2000, 3000],
            "P sample after gc [hPa]": [500, 1500, 2500],
            "CO2-corr [%]": [10.0, 15.0, 20.0],
            "CH4-corr [%]": [5.0, 7.5, 10.0]
        })
        self.Rgas = 8.314
        self.exp_temperature = 298.15
        self.volume_headspace = 10.0

    def test_mol_gas_before_sampling(self):
        MolGasCompositionCalculations.mol_gas_before_sampling(
            self.data_frame, self.Rgas, self.exp_temperature, self.volume_headspace
        )
        expected_values = [403.4179, 806.8358, 1210.2537]
        actual_values = self.data_frame["mg_bs"].tolist()
        self.assertListAlmostEqual(actual_values, expected_values, places=4)

    def test_mol_gas_after_sampling(self):
        MolGasCompositionCalculations.mol_gas_after_sampling(
            self.data_frame, self.Rgas, self.exp_temperature, self.volume_headspace
        )
        expected_values = [0.240545, 0.720653, 1.200871]
        actual_values = self.data_frame["mg_as"].tolist()
        self.assertListAlmostEqual(actual_values, expected_values)

    def test_specific_gas_in_moles_before_sampling(self):
        self.data_frame["mg_bs"] = [0.481089, 0.962178, 1.443268]
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(
            self.data_frame, "CO2-moles_bs", "mg_bs", "CO2-corr [%]"
        )
        expected_values = [0.048109, 0.096218, 0.144327]
        actual_values = self.data_frame["CO2-moles_bs"].tolist()
        self.assertListAlmostEqual(actual_values, expected_values)

    def test_carbon_total_moles(self):
        self.data_frame["CO2-moles_bs"] = [0.048109, 0.096218, 0.144327]
        self.data_frame["CH4-moles_bs"] = [0.024054, 0.072065, 0.120087]
        MolGasCompositionCalculations.carbon_total_moles(
            self.data_frame, "carbon_total_moles_bs", "CO2-moles_bs", "CH4-moles_bs"
        )
        expected_values = [0.072163, 0.168283, 0.264414]
        actual_values = self.data_frame["carbon_total_moles_bs"].tolist()
        self.assertListAlmostEqual(actual_values, expected_values)

    def assertListAlmostEqual(self, list1, list2, places=7):
        self.assertEqual(len(list1), len(list2))
        for i in range(len(list1)):
            self.assertAlmostEqual(list1[i], list2[i], places=places)


class TestMolesProduced(unittest.TestCase):
    def test_total_carbon_produced_moles(self):
        # Create a sample DataFrame
        df = pd.DataFrame({
            'Name': ['A', 'B', 'C'],
            'mCTot_b': [10, 5, 8],
            'mCTot_a': [20, 12, 15]
        })

        # Call the method under test
        MolesProduced.total_carbon_produced_moles(df, 'Total Carbon', 'mCTot_b', 'mCTot_a')

        # Assert the expected output
        expected_output = pd.DataFrame({
            'Name': ['A', 'B', 'C'],
            'mCTot_b': [10, 5, 8],
            'mCTot_a': [20, 12, 15],
            'Total Carbon': [10, 7, 7]
        })
        pd.testing.assert_frame_equal(df, expected_output)

    def test_oxygen_consumed_moles(self):
        df = pd.DataFrame({
            'mO2_b': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            'mO2_a': [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        })
        MolesProduced.oxygen_consumed_moles(df, 'result', 'mO2_b', 'mO2_a')
        expected_result = [0, 8, 6, 4, 2, 0, -2, -4, -6, -8]
        np.testing.assert_array_almost_equal(df['result'].values, expected_result)

    def test_carbon_dioxide_produced_moles(self):
        df = pd.DataFrame({
            'mCO2_b': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            'mCO2_a': [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        })
        MolesProduced.carbon_dioxide_produced_moles(df, 'result', 'mCO2_b', 'mCO2_a', 0)
        expected_result = [0, -8, -6, -4, -2, 0, 2, 4, 6, 8]
        np.testing.assert_array_almost_equal(df['result'].values, expected_result)


class TestCumulativeOperation(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'name_column_produced_or_consumed': [1, 2, 3, 4, 5],
            'name_column_flush': [0, 0, 1, 0, 1]
        })
        self.expected_output = pd.DataFrame({
            'name_column_produced_or_consumed': [1, 2, 3, 4, 5],
            'name_column_flush': [0, 0, 1, 0, 1],
            'name_column_cum': [1, 3, np.nan, 7, np.nan]
        })

    def test_cumulative_operation(self):
        CumulativeProductionGasPhase.cumulative_operation(self.data, 'name_column_cum',
                                                          'name_column_produced_or_consumed', 'name_column_flush', 0)

        pd.testing.assert_frame_equal(self.data, self.expected_output)
