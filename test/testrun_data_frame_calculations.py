import unittest

import numpy as np
import pandas as pd

from standard_gas_composition_calculations import MolesProduced, CumulativeProductionGasPhase, GasComposition, \
    MolGasCompositionCalculations, CarbonInAqueousPhase


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


class TestMolesProduced(unittest.TestCase):
    def test_total_carbon_produced_moles(self):
        mCTot_a = [
            1.32E-05, 6.20E-04, 9.74E-04, 3.25E-04, 9.95E-04, 2.81E-04, 1.72E-03,
            2.38E-03, 3.50E-04, 2.10E-03, 2.29E-04, 2.84E-03, 2.63E-04, 1.81E-03,
            1.83E-04, 1.51E-03, 1.88E-04, 1.68E-03, 1.90E-04, 1.18E-03, 1.33E-04,
            2.68E-03, 2.90E-04
        ]
        mCTot_b = [
            1.32E-05, 6.21E-04, 9.76E-04, 3.31E-04, 9.99E-04, 2.85E-04, 1.72E-03,
            2.39E-03, 3.51E-04, 2.11E-03, 2.30E-04, 2.84E-03, 2.64E-04, 1.81E-03,
            1.83E-04, 1.51E-03, 1.89E-04, 1.69E-03, 1.90E-04, 1.19E-03, 1.33E-04,
            2.68E-03, 2.91E-04
        ]
        flush = [
            np.nan, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
        ]
        m_carbont_tot_produced_in_mol = [
            0.00E+00, 6.08E-04, 3.56E-04, np.nan, 6.73E-04, np.nan, 1.44E-03, 6.72E-04,
            np.nan, 1.76E-03, np.nan, 2.62E-03, np.nan, 1.55E-03, np.nan, 1.33E-03, np.nan,
            1.51E-03, np.nan, 9.96E-04, np.nan, 2.55E-03, np.nan
        ]
        # Create a sample DataFrame
        df = pd.DataFrame({
            'mCTot_b': mCTot_b,
            'mCTot_a': mCTot_a,
            'flush': flush
        })

        # Call the method under test
        MolesProduced.total_carbon_produced_moles(data_frame=df,
                                                  name_column='Total Carbon',
                                                  name_column_mCTot_b='mCTot_b',
                                                  name_column_mCTot_a='mCTot_a',
                                                  name_column_flush="flush")

        # Assert the expected output
        expected_output = pd.DataFrame({
            'mCTot_b': mCTot_b,
            'mCTot_a': mCTot_a,
            'flush': flush,
            'Total Carbon': m_carbont_tot_produced_in_mol
        })
        df["Total Carbon"] = df["Total Carbon"].fillna(0)
        expected_output["Total Carbon"] = expected_output["Total Carbon"].fillna(0)
        self.assertIsInstance(df, pd.DataFrame)
        for i in range(1, len(flush) - 1):
            self.assertAlmostEqual(expected_output["mCTot_b"][i], df["mCTot_b"][i], places=5)
            self.assertAlmostEqual(expected_output["mCTot_a"][i], df["mCTot_a"][i], places=5)
            self.assertAlmostEqual(expected_output["flush"][i], df["flush"][i], places=5)
            self.assertAlmostEqual(expected_output["Total Carbon"][i], df["Total Carbon"][i], places=4)

    def test_oxygen_consumed_moles(self):
        df = pd.DataFrame({
            'mO2_b': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            'mO2_a': [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
            "flush": [0, 0, 1, 0, 1, 0, 0, 0, 1, 0]
        })
        MolesProduced.oxygen_consumed_moles(data_frame=df,
                                            name_column='result',
                                            name_column_mO2_b='mO2_b',
                                            name_column_mO2_a='mO2_a',
                                            name_column_flush="flush")
        expected_result = [0, 8, 0, 4, 0, 0, -2, -4, 0, -8]
        # the zeros are representing the np.nan values.
        df["result"] = df["result"].fillna(0)
        np.testing.assert_array_almost_equal(df['result'].values, expected_result)

    def test_carbon_dioxide_produced_moles(self):
        df = pd.DataFrame({
            'mCO2_b': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            'mCO2_a': [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
            "flush": [0, 0, 1, 0, 1, 0, 0, 0, 1, 0]
        })
        MolesProduced.carbon_dioxide_produced_moles(data_frame=df,
                                                    name_column='result',
                                                    name_column_mCO2_b='mCO2_b',
                                                    name_column_mCO2_a='mCO2_a',
                                                    name_column_flush="flush")
        expected_result = [0, -8, 0, -4, 0, 0, 2, 4, 0, 8]
        # the zeros are representing the np.nan values.
        df["result"] = df["result"].fillna(0)
        np.testing.assert_array_almost_equal(df['result'].values, expected_result)


class TestCumulativeOperation(unittest.TestCase):
    def setUp(self):
        self.molar_mass_carbon = 12.01
        self.dry_mass_sample = 2.5

    def test_cumulative_operation(data):
        data_frame = pd.DataFrame({
            'name_column_produced_or_consumed': [0, 2, np.nan, 4, np.nan],
            'name_column_flush': [0, 0, 1, 0, 1]
        })
        expected_output = pd.DataFrame({
            'name_column_produced_or_consumed': [0, 2, np.nan, 4, np.nan],
            'name_column_flush': [0, 0, 1, 0, 1],
            'name_column_cum': [0, 2, np.nan, 6, np.nan]
        })
        CumulativeProductionGasPhase.cumulative_operation(data_frame, 'name_column_cum',
                                                          'name_column_produced_or_consumed', 'name_column_flush', 0)
        pd.testing.assert_frame_equal(data_frame, expected_output)

    def test_carbon_gas_dry_mass_cumulative(self):
        # Create a sample DataFrame for testing
        data = {
            'name_column_flush': [0, 1, 0, 0, 1, 0],
            'name_column_mCTot_produced_cumulative': [10, 20, 30, 40, 50, 60]
        }
        df = pd.DataFrame(data)

        # Set up the expected result
        expected_result = [0, 999, 180150, 240200, 999, 360300]

        # Call the method under test
        CumulativeProductionGasPhase.carbon_gas_dry_mass_cumulative(df, 'name_column',
                                                                    'name_column_mCTot_produced_cumulative',
                                                                    12.01, 2.0, 'name_column_flush', 0)
        df["name_column"] = df["name_column"].fillna(999)
        # Check if the result matches the expected result
        self.assertListEqual(df['name_column'].tolist(), expected_result)


class TestCarbonInAqueousPhase(unittest.TestCase):
    def test_partial_pressure_carbon_dioxide_before_sampling(self):
        name_column = 'partial pressure CO2_b'
        column_name_pressure_before_sampling = "pressure before sampling"
        column_name_corrected_carbon_dioxide_in_percentage = "CO2-corr [%]"

        data = {
            column_name_pressure_before_sampling: [1117.44, 960, 962.2, 1104.6, 954],
            column_name_corrected_carbon_dioxide_in_percentage: [0.03, 1.52238806, 2.330979785, 0.759675598,
                                                                 2.625989573]
        }
        df = pd.DataFrame(data)

        CarbonInAqueousPhase.partial_pressure_carbon_dioxide_before_sampling(
            data_frame=df,
            name_column=name_column,
            column_name_pressure_before_sampling=column_name_pressure_before_sampling,
            column_name_corrected_carbon_dioxide_in_percentage=column_name_corrected_carbon_dioxide_in_percentage
        )

        expected_partial_pressure_values = [33.5232, 1461.492537, 2242.868749, 839.1376655, 2505.194053]

        for i in range(5):
            self.assertAlmostEqual(data[column_name_pressure_before_sampling][i],
                                   df[column_name_pressure_before_sampling][i], places=5)
            self.assertAlmostEqual(data[column_name_corrected_carbon_dioxide_in_percentage][i],
                                   df[column_name_corrected_carbon_dioxide_in_percentage][i], places=5)
            self.assertAlmostEqual(expected_partial_pressure_values[i],
                                   df[name_column][i], places=5)

    def test_carbon_dioxide_in_aqueous_phase_mol_per_m3(self):
        name_column = "CO2_aq [mol/m3]"
        column_name_pp_co2_bs = "partial pressure CO2_b"

        data = {column_name_pp_co2_bs: [33.5232, 1461.492537, 2242.868749, 839.1376655, 2505.194053]}
        df = pd.DataFrame(data)

        CarbonInAqueousPhase.carbon_dioxide_in_aqueous_phase_mol_per_m3(
            data_frame=df,
            name_column=name_column,
            column_name_PP_CO2_bs=column_name_pp_co2_bs
        )
        expected_values_co2_aq_mol_per_m3 = [1.753263360000000E-01,
                                             7.643605970149250E+00,
                                             1.173020355933840E+01,
                                             4.388689990760700E+00,
                                             1.310216489669820E+01,
                                             ]

        for i in range(5):
            self.assertAlmostEqual(data[column_name_pp_co2_bs][i], df[column_name_pp_co2_bs][i], places=5)
            self.assertAlmostEqual(expected_values_co2_aq_mol_per_m3[i], df[name_column][i], places=5)

    def test_carbon_dioxide_in_aqueous_phase_mol(self):
        name_column = "CO2_aq [mol]"
        column_name_co2_aq_mol_per_m3 = "CO2_aq [mol/m3]"

        data = {column_name_co2_aq_mol_per_m3: [1.753263360000000E-01,
                                                7.643605970149250E+00,
                                                1.173020355933840E+01,
                                                4.388689990760700E+00,
                                                1.310216489669820E+01,
                                                ]}
        df = pd.DataFrame(data)
        CarbonInAqueousPhase.carbon_dioxide_in_aqueous_phase_mol(
            data_frame=df,
            name_column=name_column,
            column_name_CO2_aq_in_mol_per_m3=column_name_co2_aq_mol_per_m3,
            water_volume_in_liters=0.098,
        )

        expected_values_co2_aq_mol = [1.71819809280000000E-05,
                                      7.49073385074627000E-04,
                                      1.14955994881517000E-03,
                                      4.30091619094549000E-04,
                                      1.28401215987642000E-03,
                                      ]
        for i in range(5):
            self.assertAlmostEqual(data[column_name_co2_aq_mol_per_m3][i], df[column_name_co2_aq_mol_per_m3][i], places=5)
            self.assertAlmostEqual(expected_values_co2_aq_mol[i], df[name_column][i], places=5)

    def test_carbon_dioxide_produced_aqueous_phase(self):
        name_column = "CO2_aq_produced"
        column_name_co2_aq_in_mol = "CO2_aq [mol]"

        data = {column_name_co2_aq_in_mol: [1.71819809280000000E-05,
                                            7.49073385074627000E-04,
                                            1.14955994881517000E-03,
                                            4.30091619094549000E-04,
                                            1.28401215987642000E-03,
                                            ] }
        df = pd.DataFrame(data)

        CarbonInAqueousPhase.carbon_dioxide_produced_aqueous_phase(
            data_frame=df,
            name_column=name_column,
            column_name_CO2_aq_in_mol=column_name_co2_aq_in_mol
        )

        expected_values_co2_produced = [0.00000000000000000E+00,
                                        7.31891404146627000E-04,
                                        4.00486563740539000E-04,
                                        -7.1946832972061700E-04,
                                        8.53920540781875000E-04,
                                        ]
        for i in range(5):
            self.assertAlmostEqual(data[column_name_co2_aq_in_mol][i], df[column_name_co2_aq_in_mol][i], places=5)
            self.assertAlmostEqual(expected_values_co2_produced[i], df[name_column][i], places=5)


