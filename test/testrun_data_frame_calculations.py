import unittest

import numpy as np
import pandas as pd

from standard_gas_composition_calculations import MolesProduced, CumulativeProductionGasPhase, GasComposition, \
    MolGasCompositionCalculations


class TestGasComposition(unittest.TestCase):

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


class TestMolGasCompositionCalculations(unittest.TestCase):


    def setUp(self):
        self.data_frame = pd.DataFrame({
            'Pressure': [1000, 2000, 3000],
            'CO2': [0.5, 0.8, 1.2],
            'CH4': [0.3, 0.4, 0.5]
        })
        self.Rgas = 8.314
        self.exp_temperature = 298
        self.volume_headspace = 10
        self.column_name_pressure = 'Pressure'
        self.name_column = 'MolarGasVolume'
        self.name_column_mg_before_or_after = 'MolarGasBeforeOrAfter'
        self.name_column_specific_gas_corrected = 'SpecificGasCorrected'
        self.name_column_CO2 = 'CO2'
        self.name_column_CH4 = 'CH4'

    def assertListAlmostEqual(self, list1, list2, places=7):
        """
        Helper function to compare two lists of floats with given precision
        """
        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, places)

    def test_mol_gas_sampling(self):
        MolGasCompositionCalculations.mol_gas_sampling(
            self.data_frame,
            self.Rgas,
            self.exp_temperature,
            self.volume_headspace,
            self.column_name_pressure,
            self.name_column
        )
        expected_values = [403.620964, 807.241928, 1210.862892]
        actual_values = self.data_frame[self.name_column].tolist()
        self.assertListAlmostEqual(actual_values, expected_values, places=5)

    def test_specific_gas_in_moles_before_sampling(self):
        self.data_frame[self.name_column_mg_before_or_after] = [0.1, 0.2, 0.3]
        self.data_frame[self.name_column_specific_gas_corrected] = [0.5, 0.7, 0.9]
        MolGasCompositionCalculations.specific_gas_in_moles_before_sampling(
            self.data_frame,
            self.name_column,
            self.name_column_mg_before_or_after,
            self.name_column_specific_gas_corrected
        )
        expected_result = pd.Series([0.0005, 0.0014, 0.0027])
        actual_values = self.data_frame[self.name_column].tolist()
        self.assertListAlmostEqual(actual_values, expected_result, places=5)

    def test_carbon_total_moles(self):
        MolGasCompositionCalculations.carbon_total_moles(
            self.data_frame,
            self.name_column,
            self.name_column_CO2,
            self.name_column_CH4
        )
        expected_result = pd.Series([0.8, 1.2, 1.7])
        actual_values = self.data_frame[self.name_column].tolist()
        self.assertListAlmostEqual(actual_values, expected_result, places=5)

    def testen(self):
        pass

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
