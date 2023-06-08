import warnings

import numpy as np
import pandas as pd


class GasComposition:
    """
    A class for setting the gas composition in the pandas DataFrame.
    """

    @staticmethod
    def set_gas_composition(data_frame: pd.DataFrame, ch4: float, co2: float, o2: float, n2: float,
                            index: int = 0) -> None:
        """
        Set the values of CH4, CO2, O2 and N2 in the DataFrame.

        :param data_frame: The data frame to do the operation for.
        :param ch4: The value of CH4 in [%].
        :param co2: The value of CO2 in [%].
        :param o2: The value of O2 in [%].
        :param n2: The value of N2 in [%].
        :param index: The index of the row to set the values. Default is 0.
        """

        data_frame.loc[index, ["CH4 [%]", "CO2 [%]", "O2 [%]", "N2 [%]"]] = [ch4, co2, o2, n2]

    @staticmethod
    def sum_correct_sum(data_frame: pd.DataFrame) -> None:
        """
        Corrects the measuring values so that the sum is 100% in the DataFrame.
        """
        df = data_frame

        # summation of the measuring values CH4, CO2, O2, N2 in [%]
        df["Sum [%]"] = df["CH4 [%]"] + df["CO2 [%]"] + df["O2 [%]"] + df["N2 [%]"]

        # Correct the measuring values so that the sum is 100%
        for i in ["CH4", "CO2", "O2", "N2"]:
            df[f"{i}-corr [%]"] = (100 / df["Sum [%]"]) * df[f"{i} [%]"]

        # The summation of the corrected values CH4, CO2, O2, N2. Must all be equal to 100%
        df["Sum-corr [%]"] = df["CH4-corr [%]"] + df["CO2-corr [%]"] + df["O2-corr [%]"] + df["N2-corr [%]"]


# This class is not used.
class PercentageO2ConsumedAndCO2ProducedAndRatio:
    """
    A class for performing calculations on the pandas DataFrame fot he gas chromatograph
    """

    @staticmethod
    def calculate_o2_consumed(data_frame: pd.DataFrame) -> None:
        """
        Calculates the O2 consumed between two periods and adds the result to the DataFrame.

        The calculation and conditions:
        Only when there was no flush the calculation is done.
        The calculation is for example: -(row_4_O2_[%] - row_3_O2_[%]) --> -(2-8) = 6
        which means that it is expected that the O2% is going down. This gives a negative value.
        To get a positive value in the context of producing the value is turned positive via the minus-sign.
        Note: a negative value means that the O2% is increased so no consumption.

        """
        data_frame["O2 consumed [%]"] = np.where(data_frame["Flush (1=yes; 0=no)"] == 0,
                                                 -data_frame["O2-corr [%]"].diff(),
                                                 np.NaN,
                                                 )

    @staticmethod
    def calculate_co2_produced(data_frame: pd.DataFrame) -> None:
        """
        Calculates the CO2 produced and adds the result to the DataFrame.

        The calculation and conditions:
        Only when there was no flush the calculation is done.
        The calculation is for example: (row_4_CO2_[%] - row3_CO2_[%]) --> (8-6) = 2
        which means that it is expected that the CO2% is going up. This gives a positive value.
        Note: a negative value means that the CO2% is decreased so no production.

        """
        data_frame["CO2 produced [%]"] = np.where(data_frame["Flush (1=yes; 0=no)"] == 0,
                                                  data_frame["CO2-corr [%]"].diff(),
                                                  np.NaN,
                                                  )

    # Is not used in the code
    @staticmethod
    def calculate_ratio_o2_co2(data_frame: pd.DataFrame) -> None:
        """
        Calculates the ratio between O2 and CO2 and adds the result to the DataFrame.

        The calculation:
        Ratio [%] = O2-consumed [%] / CO2-produced [%]
        """
        data_frame["Ratio O2/CO2 [%]"] = (data_frame["O2 consumed [%]"] / data_frame["CO2 produced [%]"])


class MolGasCompositionCalculations:
    """"In this class the calculations are done to translate the gas composition in moles.
    This is based on the ideal gas law."""

    @staticmethod
    def mol_gas_sampling(data_frame: pd.DataFrame,
                         Rgas: float,
                         exp_temperature: float,
                         volume_headspace: float,
                         column_name_pressure: str,
                         name_column: str) -> None:
        """
        Calculate the molar gas volume in the given data frame.

        Parameters
        ----------
        data_frame : pd.DataFrame
            The DataFrame containing the pressure data.
        Rgas : float
            Gas constant value.
        exp_temperature : float
            Experimental temperature value.
        volume_headspace : float
            Volume of the headspace.
        column_name_pressure : str
            Column name in the DataFrame for the pressure data.
        name_column : str
            Name of the column to be created/updated with the calculated molar gas values.

        Returns
        -------
        None
            The function updates the DataFrame in-place, it does not return a value.
        """
        constant = 100 * volume_headspace / (Rgas * exp_temperature)
        data_frame[name_column] = data_frame[column_name_pressure] * constant

    @staticmethod
    def specific_gas_in_moles_before_sampling(data_frame: pd.DataFrame,
                                              name_column: str,
                                              name_column_mg_before_or_after: str,
                                              name_column_specific_gas_corrected: str
                                              ) -> None:
        data_frame[name_column] = data_frame[name_column_mg_before_or_after] * \
                                  data_frame[name_column_specific_gas_corrected] * (1 / 100)

    @staticmethod
    def carbon_total_moles(data_frame: pd.DataFrame, name_column: str, name_column_CO2: str,
                           name_column_CH4: str) -> None:
        data_frame[name_column] = data_frame[name_column_CO2] + data_frame[name_column_CH4]


class MolesProduced:
    """"In this class the total moles produced are calculated"""

    @staticmethod
    def total_carbon_produced_moles(data_frame: pd.DataFrame, name_column: str,
                                    name_column_mCTot_b: str, name_column_mCTot_a: str,
                                    name_column_flush: str, first_row_value: float = 0) -> None:
        data_frame[name_column] = data_frame[name_column_mCTot_b] - data_frame[name_column_mCTot_a].shift(1)
        data_frame[name_column].at[0] = first_row_value

        mask = (data_frame[name_column_flush] == 1)
        data_frame.loc[mask, name_column] = np.nan

    @staticmethod
    def oxygen_consumed_moles(data_frame: pd.DataFrame, name_column: str, name_column_mO2_b: str,
                              name_column_flush: str, name_column_mO2_a: str, first_row_value: float = 0) -> None:
        """
        Compute the oxygen consumed moles and add the result to a new column in the DataFrame.
        Note that if the values are positive that the there is O2 consumed and if it is negative than produced.

        Parameters:
        data_frame (pd.DataFrame): DataFrame which includes columns for the calculation.
        name_column (str): Name of the new column where the result will be stored.
        name_column_mCTot_b (str): column name for the O2 in moles before sampling
        name_column_mCTot_a (str): column name for the O2 in moles after sampling
        """
        if not all(col in data_frame.columns for col in [name_column_mO2_b, name_column_mO2_a]):
            raise ValueError("All specified columns must be present in the DataFrame")

        data_frame[name_column] = (data_frame[name_column_mO2_b] - data_frame[name_column_mO2_a].shift(1)) * -1
        data_frame[name_column].at[0] = first_row_value

        mask = (data_frame[name_column_flush] == 1)
        data_frame.loc[mask, name_column] = np.nan

    @staticmethod
    def carbon_dioxide_produced_moles(data_frame: pd.DataFrame, name_column: str,
                                      name_column_mCO2_b: str, name_column_mCO2_a: str,
                                      name_column_flush: str, first_row_value: float = 0) -> None:
        """
        Compute the oxygen consumed moles and add the result to a new column in the DataFrame.
        Note that if the values are positive that there is O2 consumed and if it is negative than produced.

        Parameters:
        data_frame (pd.DataFrame): DataFrame which includes columns for the calculation.
        name_column (str): Name of the new column where the result will be stored.
        name_column_mCTot_b (str): column name for the CO2 in moles before sampling
        name_column_mCTot_a (str): column name for the CO2 in moles after sampling
        first_row_value (float): Value to be assigned to the first row of the new column.
        """
        if not all(col in data_frame.columns for col in [name_column_mCO2_b, name_column_mCO2_a]):
            raise ValueError("All specified columns must be present in the DataFrame")

        data_frame[name_column] = (data_frame[name_column_mCO2_b] - data_frame[name_column_mCO2_a].shift(1))
        data_frame[name_column].at[0] = first_row_value

        mask = (data_frame[name_column_flush] == 1)
        data_frame.loc[mask, name_column] = np.nan


class CumulativeProductionGasPhase:
    @staticmethod
    def cumulative_operation(data_frame: pd.DataFrame, name_column_cum: str,
                             name_column_produced_or_consumed: str,
                             name_column_flush: str,
                             first_row_value: float = 0) -> None:
        """
        This cumulative operation is especially for the gas measurements with flushing.

        :param data_frame: the input data frame for the operations.
        :param name_column_cum: the name of the new created column for the cumulative values.
        :param name_column_produced_or_consumed: the name of the values to be cumulated.
        :param name_column_flush: the name of the flush column (zeros and ones)
        :param first_row_value: the value for the first row.
        """
        # Initialize column with NaN
        data_frame[name_column_cum] = np.nan

        # Set the first row's cumulative value
        data_frame[name_column_cum].at[0] = first_row_value

        # cumulative calculation with the flush conditions. With the last_non_flush_index the index of the last flush
        # is stored and that corresponding value can be called.
        last_non_flush_index = 0
        for index_row in range(1, len(data_frame)):
            if data_frame.loc[index_row, name_column_flush] == 0:
                data_frame.loc[index_row, name_column_cum] = data_frame.loc[last_non_flush_index, name_column_cum] + \
                                                             data_frame.loc[index_row, name_column_produced_or_consumed]
                last_non_flush_index = index_row
            elif data_frame.loc[index_row, name_column_flush] == 1:
                data_frame.loc[index_row, name_column_cum] = np.nan
            else:
                warnings.warn("Unknown value for flush, must be zero or one" + str(index_row))

    @staticmethod
    def carbon_gas_dry_mass_cumulative(data_frame: pd.DataFrame, name_column: str,
                                       name_column_mCTot_produced_cumulative: str,
                                       molar_mass_carbon: float,
                                       dry_mass_sample: float,
                                       name_column_flush: str,
                                       first_row_value: float = 0) -> None:

        constant = molar_mass_carbon * (1000 / dry_mass_sample)
        data_frame[name_column] = np.where(data_frame[name_column_flush] == 0,
                                           data_frame[name_column_mCTot_produced_cumulative] * constant,
                                           np.nan)

        # Set the first row's cumulative value
        data_frame[name_column].at[0] = first_row_value


class CarbonInAqueousPhase:
    @staticmethod
    def partial_pressure_carbon_dioxide_before_sampling(data_frame: pd.DataFrame, name_column,
                                                        column_name_pressure_before_sampling: str,
                                                        column_name_corrected_carbon_dioxide_in_percentage: str
                                                        ) -> None:
        data_frame[name_column] = data_frame[column_name_pressure_before_sampling] * 100 * \
                                  data_frame[column_name_corrected_carbon_dioxide_in_percentage] / 100

    @staticmethod
    def carbon_dioxide_in_aqueous_phase_mol_per_m3(data_frame: pd.DataFrame, name_column: str,
                                                   column_name_PP_CO2_bs: str,
                                                   henry_law_constant: float = (5.23 * 10 ** -3)) -> None:
        """
        :param data_frame: pd.DataFrame
        :param name_column: column name for the new created column for the calculation/
        :param column_name_PP_CO2_bs: The column name partial pressure carbon dioxide before sampling.
        :param henry_law_constant: constant of the Henry law for CO2. Default at 20 degrees.

        Return:
        carbon dioxide in aqueous phase [mol/m3] in a new column in the data frame pandas

        """
        data_frame[name_column] = data_frame[column_name_PP_CO2_bs] * henry_law_constant

    @staticmethod
    def carbon_dioxide_in_aqueous_phase_mol(data_frame: pd.DataFrame, name_column: str,
                                            column_name_CO2_aq_in_mol_per_m3: str,
                                            water_volume_in_liters: float) -> None:
        data_frame[name_column] = data_frame[column_name_CO2_aq_in_mol_per_m3] * (water_volume_in_liters / 1000)

    @staticmethod
    def carbon_dioxide_produced_aqueous_phase(data_frame: pd.DataFrame, name_column: str,
                                              column_name_CO2_aq_in_mol: str,
                                              first_row_value: float = 0) -> None:
        data_frame[name_column] = data_frame[column_name_CO2_aq_in_mol] - data_frame[column_name_CO2_aq_in_mol].shift(1)

        data_frame[name_column].at[0] = first_row_value

    @staticmethod
    def dissolved_inorganic_carbon_cumulative(data_frame: pd.DataFrame, name_column: str,
                                              column_name_CO2_aq_in_mol_per_m3: str,
                                              dry_mass_sample: float,
                                              water_volume_in_liters: float,
                                              molar_mass_carbon: float = 12
                                              ):
        """

        :type molar_mass_carbon: molar mass of carbon. is constant and set to 12 g/mol
        """
        constant = molar_mass_carbon * (water_volume_in_liters / dry_mass_sample)
        data_frame[name_column] = np.nan
        # set the first value
        data_frame[name_column].at[0] = data_frame[column_name_CO2_aq_in_mol_per_m3].at[0] * constant

        data_frame[name_column][1:] = (data_frame[column_name_CO2_aq_in_mol_per_m3][1:] * constant) - data_frame[name_column].at[0]


class ResultsInterpretations:

    @staticmethod
    def total_carbon_dry_matter(data_frame: pd.DataFrame, name_column: str, name_column_flush: str,
                                name_column_C_gas_dry_mass_cum: str, name_column_DIC_cum: str,
                                first_row_value: float = 0) -> None:
        data_frame[name_column] = np.nan
        data_frame[name_column].at[0] = first_row_value

        data_frame[name_column][1:] = data_frame[name_column_C_gas_dry_mass_cum][1:] + data_frame[name_column_DIC_cum][1:]

        mask = (data_frame[name_column_flush] == 1)
        data_frame.loc[mask, name_column] = np.nan

    @staticmethod
    def ratio_oxygen_consumed_carbon_dioxide_produced(data_frame: pd.DataFrame, name_column: str,
                                                      name_column_O2_consumed_mol: str,
                                                      name_column_CO2_produced_gas_mol: str,
                                                      name_column_CO2_produced_aqueous_mol: str,
                                                      name_column_flush: str, first_row_value: float = 0
                                                      ):
        data_frame[name_column] = data_frame[name_column_O2_consumed_mol] / (
                data_frame[name_column_CO2_produced_gas_mol] + data_frame[name_column_CO2_produced_aqueous_mol])

        data_frame[name_column].at[0] = first_row_value
        mask = (data_frame[name_column_flush] == 1)
        data_frame.loc[mask, name_column] = np.nan
