import unittest

import pandas as pd

from data_frame_calculations_standard_for_gas_respiration_tests import GasComposition, MolGasCompositionCalculations


class TestGasComposition(unittest.TestCase):

    def test_set_gas_composition(self):
        data_frame = pd.DataFrame(columns=["CH4 [%]", "CO2 [%]", "O2 [%]", "N2 [%]"])
        GasComposition.set_gas_composition(data_frame, 10.0, 20.0, 30.0, 40.0)
        expected_values = [10.0, 20.0, 30.0, 40.0]
        actual_values = data_frame.loc[0, ["CH4 [%]", "CO2 [%]", "O2 [%]", "N2 [%]"]].tolist()
        self.assertEqual(actual_values, expected_values)

    def test_sum_correct_sum(self):
        data_frame = pd.DataFrame({
            "CH4 [%]": [12.0, 18.0, 30.0],
            "CO2 [%]": [33.0, 17.0, 10.0],
            "O2 [%]": [35.0, 39.0, 10.0],
            "N2 [%]": [30.0, 16.0, 50.0]
        })
        GasComposition.sum_correct_sum(data_frame)
        expected_values_sum = [110, 90, 100]
        actual_values_sum = data_frame["Sum [%]"].tolist()
        self.assertEqual(expected_values_sum, actual_values_sum)

        expected_values_sum_corr = [100, 100, 100]
        actual_values_sum_corr = data_frame["Sum-corr [%]"].tolist()
        self.assertEqual(expected_values_sum_corr, actual_values_sum_corr)

        # check for every gas
        ch4_corr_list_expected = [10.90909, 20, 30]
        co2_corr_list_expected = [30.00000, 18.888889, 10]
        o2_corr_list_expected = [31.818182, 43.333333, 10]
        n2_corr_list_expected = [27.27273, 17.777778, 50]

        for i in range(3):
            self.assertAlmostEqual(ch4_corr_list_expected[i], data_frame["CH4-corr [%]"][i], places=5)
            self.assertAlmostEqual(co2_corr_list_expected[i], data_frame["CO2-corr [%]"][i], places=5)
            self.assertAlmostEqual(o2_corr_list_expected[i], data_frame["O2-corr [%]"][i], places=5)
            self.assertAlmostEqual(n2_corr_list_expected[i], data_frame["N2-corr [%]"][i], places=5)


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
