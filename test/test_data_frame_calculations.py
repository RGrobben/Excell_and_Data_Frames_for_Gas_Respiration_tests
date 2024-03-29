import unittest

import numpy as np
import pandas as pd

from data_frame_calculations import MolesProduced, CumulativeProductionGasPhase, CarbonInAqueousPhase, ResultsInterpretations


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

        CarbonInAqueousPhase.partial_pressure_carbon_dioxide(
            data_frame=df,
            name_column=name_column,
            column_name_pressure_sampling=column_name_pressure_before_sampling,
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
            column_name_PP_CO2=column_name_pp_co2_bs
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
            self.assertAlmostEqual(data[column_name_co2_aq_mol_per_m3][i], df[column_name_co2_aq_mol_per_m3][i],
                                   places=5)
            self.assertAlmostEqual(expected_values_co2_aq_mol[i], df[name_column][i], places=5)

    def test_carbon_dioxide_produced_aqueous_phase(self):
        name_column = "CO2_aq_produced"
        column_name_co2_aq_in_mol = "CO2_aq [mol]"

        data = {column_name_co2_aq_in_mol: [1.71819809280000000E-05,
                                            7.49073385074627000E-04,
                                            1.14955994881517000E-03,
                                            4.30091619094549000E-04,
                                            1.28401215987642000E-03,
                                            ]}
        df = pd.DataFrame(data)

        CarbonInAqueousPhase.carbon_dioxide_produced_aqueous_phase_cumulative(
            data_frame=df,
            name_column=name_column,
            carbon_dioxide_dissolved_between_time_steps_aqueous=column_name_co2_aq_in_mol
        )

        expected_values_co2_produced = [1.7181980928e-05,
                                        0.0007662553660026269,
                                        0.0019158153148177968,
                                        0.002345906933912346,
                                        0.003629919093788766,
                                        ]
        for i in range(5):
            self.assertAlmostEqual(data[column_name_co2_aq_in_mol][i], df[column_name_co2_aq_in_mol][i], places=3)
            self.assertAlmostEqual(expected_values_co2_produced[i], df[name_column][i], places=5)

    def test_dissolved_inorganic_carbon_cumulative(self):
        name_column = "DIC_cum"
        column_name_co2_aq_in_mol_per_m3 = "CO2_aq [mol/m3]"

        data = {column_name_co2_aq_in_mol_per_m3: [1.753263360000000 * 10 ** -1,
                                                   7.643605970149250,
                                                   1.173020355933840 * 10 ** 1,
                                                   4.388689990760700,
                                                   1.310216489669820 * 10 ** 1,
                                                   ]}
        df = pd.DataFrame(data)

        CarbonInAqueousPhase.dissolved_inorganic_carbon_cumulative(
            data_frame=df,
            name_column=name_column,
            column_name_CO2_aq_in_mol_per_m3=column_name_co2_aq_in_mol_per_m3,
            dry_mass_sample=153.6,
        )

        expected_values_dic_cum = [13.697370000000003,
                                   597.1567164179102,
                                   916.4221530733124,
                                   342.8664055281797,
                                   1023.6066325545469,
                                   ]

        for i in range(5):
            self.assertAlmostEqual(data[column_name_co2_aq_in_mol_per_m3][i], df[column_name_co2_aq_in_mol_per_m3][i],
                                   places=5)
            self.assertAlmostEqual(expected_values_dic_cum[i], df[name_column][i], places=3)

    def test_carbon_dioxide_dissolved_between_time_steps_aqueous(self):
        column_name = "difference"
        column_name_CO2_before_aq_in_mol = "CO_2 before",
        column_name_CO2_after_aq_in_mol = "CO2_after"

        # Prepare a data frame for testing
        df = pd.DataFrame({
            column_name_CO2_before_aq_in_mol: [10, 20, 30, 40, 53],
            column_name_CO2_after_aq_in_mol: [5, 15, 20, 35, 44]
        })

        expected_output = pd.Series([5, 15, 15, 20, 18])
        # Run the method to be tested
        CarbonInAqueousPhase.carbon_dioxide_dissolved_between_time_steps_aqueous(data_frame=df,
                                                                                 name_column=column_name,
                                                                                 column_name_CO2_before_aq_in_mol=
                                                                                 column_name_CO2_before_aq_in_mol,
                                                                                 column_name_CO2_after_aq_in_mol=
                                                                                 column_name_CO2_after_aq_in_mol)

        # Check if the results are as expected
        for i in range(5):
            print(expected_output[i], df[column_name][i])
            self.assertAlmostEqual(expected_output[i], df[column_name][i], places=5)


class TestResultsInterpretations(unittest.TestCase):
    def test_total_carbon_dry_matter(self):
        name_column = "Tot Carbon dry matter"
        name_column_flush = "flush"
        name_column_c_gas_dry_mass_cum = "Cgas_DM_cum "
        name_column_dic_cum = "DIC_cum"

        data = {name_column_flush: [np.nan, 0, 0, 1, 0],
                name_column_c_gas_dry_mass_cum: [0.00E+00, 4.75E-02, 7.53E-02, np.nan, 1.28E-01],
                name_column_dic_cum: [1.342274225973880E-03,
                                      5.717611794091300E-02,
                                      8.846254496061420E-02,
                                      3.225693051864370E-02,
                                      9.896609157080900E-02]
                }
        df = pd.DataFrame(data)

        ResultsInterpretations.total_carbon_dry_matter(
            data_frame=df,
            name_column=name_column,
            name_column_flush=name_column_flush,
            name_column_C_gas_dry_mass_cum=name_column_c_gas_dry_mass_cum,
            name_column_DIC_cum=name_column_dic_cum
        )

        # 999_999 represents np.nan
        expected_values_total_carbon_dry_matter = [0.0000000000000000E+00,
                                                   1.0468968410856200E-01,
                                                   1.6377501873632500E-01,
                                                   999_999,
                                                   2.2688578876849800E-01,
                                                   ]
        df[name_column] = df[name_column].fillna(999_999)
        df[name_column_flush] = df[name_column_flush].fillna(999)

        for i in range(5):
            self.assertAlmostEqual(data[name_column_dic_cum][i], df[name_column_dic_cum][i], places=5)
            self.assertAlmostEqual(expected_values_total_carbon_dry_matter[i], df[name_column][i], places=3)

    def test_ratio_oxygen_consumed_carbon_dioxide_produced(self):
        name_column = "Ratio O2/CO2"
        name_column_o2_consumed_mol = "O2 consumed mol"
        name_column_co2_produced_gas_mol = "CO2 gas produced mol"
        name_column_co2_produced_aqueous_mol = "CO2_aq produced mol",
        name_column_flush = "flush"

        data = {name_column_o2_consumed_mol: [0.00E+00, 0.008816302, 0.000247261, np.nan, 0.005625266],
                name_column_co2_produced_gas_mol: [0.00E+00, 0.00056301, 0.000309216, np.nan, 0.000662512],
                name_column_co2_produced_aqueous_mol: [0.00000000000000000E+00,
                                                       7.31891404146627000E-04,
                                                       4.00486563740539000E-04,
                                                       -7.19468329720617000E-04,
                                                       8.53920540781875000E-04
                                                       ],
                name_column_flush: [np.nan, 0, 0, 1, 0]
                }
        df = pd.DataFrame(data)

        ResultsInterpretations.ratio_oxygen_consumed_carbon_dioxide_produced(
            data_frame=df,
            name_column=name_column,
            name_column_O2_consumed_mol=name_column_o2_consumed_mol,
            name_column_CO2_produced_gas_mol=name_column_co2_produced_gas_mol,
            carbon_dioxide_dissolved_between_time_steps_aqueous=name_column_co2_produced_aqueous_mol,
            name_column_flush=name_column_flush
        )

        expected_values_ratio = [0.0000000000000000E+00, 6.8084727628589200E+00, 3.4840115566368000E-01,
                                 999_999, 3.7095378263987700E+00]
        # 999_999 represents np.nan
        df[name_column] = df[name_column].fillna(999_999)
        df[name_column_flush] = df[name_column_flush].fillna(999)

        for i in range(5):
            self.assertAlmostEqual(expected_values_ratio[i], df[name_column][i], places=3)
