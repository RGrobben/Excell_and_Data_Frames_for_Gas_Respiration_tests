import unittest

import numpy as np
import pandas as pd

from standard_gas_composition_calculations import MolesProduced, CumulativeProductionGasPhase


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
