import warnings

import numpy as np
import pandas as pd


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


class MolesProduced:
    """"In this class the total moles produced are calculated"""

    @staticmethod
    def total_carbon_produced_moles(data_frame: pd.DataFrame, name_column: str,
                                    name_column_mCTot_b: str, name_column_mCTot_a: str,
                                    name_column_flush: str, first_row_value: float = 0) -> None:
        """
            Calculate the total moles of carbon produced in the DataFrame.

            Parameters:
                - data_frame (pd.DataFrame): The DataFrame to modify.
                - name_column (str): The name of the column to store the calculated total moles of carbon produced [mol]
                - name_column_mCTot_b (str): The name of the column containing the cumulative carbon
                gas produced (after sampling). [mol]
                - name_column_mCTot_a (str): The name of the column containing the cumulative carbon
                gas produced (before sampling). [mol]
                - name_column_flush (str): The name of the column used for flushing indication.
                - first_row_value (float, optional): The value to set for the first row of the total
                carbon produced column. Defaults to 0.

            Returns:
                None
            """
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
        name_column (str): Name of the new column where the result will be stored. [mol]
        name_column_mCTot_b (str): column name for the O2 in moles before sampling [mol]
        name_column_mCTot_a (str): column name for the O2 in moles after sampling [mol]
        """
        # if not all(col in data_frame.columns for col in [name_column_mO2_b, name_column_mO2_a]):
        #     raise ValueError("All specified columns must be present in the DataFrame")

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
        name_column (str): Name of the new column where the result will be stored. [mol]
        name_column_mCTot_b (str): column name for the CO2 in moles before sampling [mol]
        name_column_mCTot_a (str): column name for the CO2 in moles after sampling [mol]
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
        :param name_column_cum: the name of the new created column for the cumulative values. [mol]
        :param name_column_produced_or_consumed: the name of the values to be cumulated. [mol]
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
        """
            Calculate the cumulative carbon gas dry mass in the DataFrame.

            Parameters:
                - data_frame (pd.DataFrame): The DataFrame to modify.
                - name_column (str): The name of the column to store the calculated cumulative carbon gas dry mass \
                [mg C/g DW (Dry Weight)]
                - name_column_mCTot_produced_cumulative (str): The name of the column containing the cumulative
                carbon gas produced. [mol]
                - molar_mass_carbon (float): The molar mass of carbon. [g / mol]
                - dry_mass_sample (float): The dry mass of the sample. [g]
                - name_column_flush (str): The name of the column used for flushing indication.
                - first_row_value (float, optional): The value to set for the first row of the cumulative column.
                Defaults to 0.

            Returns:
                None
            """

        constant = molar_mass_carbon * (1000 / dry_mass_sample)
        data_frame[name_column] = np.where(data_frame[name_column_flush] == 0,
                                           data_frame[name_column_mCTot_produced_cumulative] * constant,
                                           np.nan)

        # Set the first row's cumulative value
        data_frame[name_column].at[0] = first_row_value


class CarbonInAqueousPhase:
    @staticmethod
    def partial_pressure_carbon_dioxide(data_frame: pd.DataFrame, name_column,
                                        column_name_pressure_sampling: str,
                                        column_name_corrected_carbon_dioxide_in_percentage: str
                                        ) -> None:
        """
            Calculate the partial pressure of carbon dioxide in the DataFrame.

            Parameters:
                - data_frame (pd.DataFrame): The DataFrame to modify.
                - name_column (str):
                The name of the column to store the calculated partial pressure of carbon dioxide.[Pa]
                - column_name_pressure_sampling (str):
                The name of the column containing the pressure during sampling. [hPa]
                - column_name_corrected_carbon_dioxide_in_percentage (str):
                The name of the column containing the corrected carbon dioxide in percentage. [%]

            Returns:
                None
            """
        if np.isnan(data_frame.at[0, column_name_pressure_sampling]):
            data_frame.at[0, column_name_pressure_sampling] = 0

        data_frame[name_column] = data_frame[column_name_pressure_sampling] * 100 * \
                                  data_frame[column_name_corrected_carbon_dioxide_in_percentage] / 100

    @staticmethod
    def carbon_dioxide_in_aqueous_phase_mol_per_m3(data_frame: pd.DataFrame, name_column: str,
                                                   column_name_PP_CO2: str,
                                                   henry_law_constant: float = (5.23 * 10 ** -3)) -> None:
        """
        :param data_frame: pd.DataFrame
        :param name_column: column name for the new created column for the calculation. [mol/m3]
        :param column_name_PP_CO2: The column name partial pressure carbon dioxide  sampling. [Pa]
        :param henry_law_constant: constant of the Henry law for CO2. Default at 20 degrees.

        Return:
        carbon dioxide in aqueous phase [mol/m3] in a new column in the data frame pandas

        """
        data_frame[name_column] = data_frame[column_name_PP_CO2] * henry_law_constant

    @staticmethod
    def carbon_dioxide_in_aqueous_phase_mol(data_frame: pd.DataFrame, name_column: str,
                                            column_name_CO2_aq_in_mol_per_m3: str,
                                            water_volume_in_liters: float) -> None:
        """
            Calculate the amount of carbon dioxide in the aqueous phase in moles in the DataFrame.

            Parameters:
                - data_frame (pd.DataFrame): The DataFrame to modify.
                - name_column (str):
                The name of the column to store the calculated amount of carbon dioxide in the aqueous phase. [mol]
                - column_name_CO2_aq_in_mol_per_m3 (str):
                The name of the column containing the carbon dioxide in moles per cubic meter. [mol/m3]
                - water_volume_in_liters (float): The volume of water in liters. [l]

            Returns:
                None
            """
        data_frame[name_column] = data_frame[column_name_CO2_aq_in_mol_per_m3] * (water_volume_in_liters / 1000)

    @staticmethod
    def carbon_dioxide_dissolved_between_time_steps_aqueous(data_frame: pd.DataFrame, name_column: str,
                                                            column_name_CO2_before_aq_in_mol: str,
                                                            column_name_CO2_after_aq_in_mol: str) -> None:
        """
            Calculate the amount of carbon dioxide dissolved between time steps in the aqueous phase in the DataFrame.

            Parameters:
                - data_frame (pd.DataFrame): The DataFrame to modify.
                - name_column (str): The name of the column to store the calculated amount of carbon dioxide
                dissolved in the aqueous phase. [mol]
                - column_name_CO2_before_aq_in_mol (str): The name of the column containing the carbon dioxide
                in moles in the aqueous phase (before time step). [mol]
                - column_name_CO2_after_aq_in_mol (str): The name of the column containing the carbon dioxide
                in moles in the aqueous phase (after time step). [mol]

            Returns:
                None
            """
        data_frame[name_column] = data_frame[column_name_CO2_before_aq_in_mol] - \
                                  data_frame[column_name_CO2_after_aq_in_mol].shift(1)

        data_frame.loc[0, name_column] = data_frame[column_name_CO2_before_aq_in_mol].at[0] - \
                                         data_frame[column_name_CO2_after_aq_in_mol].at[0]

    @staticmethod
    def carbon_dioxide_produced_aqueous_phase_cumulative(data_frame: pd.DataFrame, name_column: str,
                                                         carbon_dioxide_dissolved_between_time_steps_aqueous: str) -> None:
        """
            Calculate the cumulative amount of carbon dioxide produced in the aqueous phase in the DataFrame.

            Parameters:
                - data_frame (pd.DataFrame): The DataFrame to modify.
                - name_column (str): The name of the column to store the calculated cumulative amount of carbon
                dioxide produced in the aqueous phase. [mol]
                - carbon_dioxide_dissolved_between_time_steps_aqueous (str): The name of the column containing
                the amount of carbon dioxide dissolved between time steps in the aqueous phase. [mol]

            Returns:
                None
            """
        data_frame[name_column] = data_frame[carbon_dioxide_dissolved_between_time_steps_aqueous].cumsum()

    @staticmethod
    def dissolved_inorganic_carbon_cumulative(data_frame: pd.DataFrame, name_column: str,
                                              column_name_CO2_aq_in_mol_per_m3: str,
                                              dry_mass_sample: float,
                                              molar_mass_carbon: float = 12
                                              ):
        """
            Calculate the cumulative dissolved inorganic carbon in the DataFrame.

            Parameters:
                - data_frame (pd.DataFrame): The DataFrame to modify.
                - name_column (str): The name of the column to store the calculated cumulative
                dissolved inorganic carbon. [mg C/g DW (Dry Weight)]
                - column_name_CO2_aq_in_mol_per_m3 (str): The name of the column containing the
                carbon dioxide in moles per cubic meter in the aqueous phase. [mol/m3]
                - dry_mass_sample (float): The dry mass of the sample. [g]
                - molar_mass_carbon (float, optional): The molar mass of carbon. Defaults to 12 g/mol. [g/mol]

            Returns:
                None
            """
        gram_to_mmg = 1000
        constant = molar_mass_carbon * (gram_to_mmg / dry_mass_sample)

        data_frame[name_column] = (data_frame[column_name_CO2_aq_in_mol_per_m3] * constant)


class ResultsInterpretations:

    @staticmethod
    def total_carbon_dry_matter(data_frame: pd.DataFrame, name_column: str, name_column_flush: str,
                                name_column_C_gas_dry_mass_cum: str, name_column_DIC_cum: str,
                                first_row_value: float = 0) -> None:
        """
           Calculate the total carbon dry matter in the DataFrame.

           Parameters:
               - data_frame (pd.DataFrame): The DataFrame to modify.
               - name_column (str): The name of the column to store the calculated total carbon
               dry matter. [mg C/g DW (Dry Weight)]
               - name_column_flush (str): The name of the column used for flushing indication.
               - name_column_C_gas_dry_mass_cum (str): The name of the column containing the cumulative
               carbon gas dry mass. [mg C/g DW (Dry Weight)]
               - name_column_DIC_cum (str): The name of the column containing the cumulative dissolved inorganic carbon.
               [mg C/g DW (Dry Weight)]
               - first_row_value (float, optional): The value to set for the first row of the total carbon
               dry matter column. Defaults to 0.

           Returns:
               None
           """
        data_frame[name_column] = np.nan
        data_frame[name_column].at[0] = first_row_value

        data_frame.loc[1:, name_column] = data_frame.loc[1:, name_column_C_gas_dry_mass_cum] + data_frame.loc[1:,
                                                                                               name_column_DIC_cum]

        mask = (data_frame[name_column_flush] == 1)
        data_frame.loc[mask, name_column] = np.nan

    @staticmethod
    def ratio_oxygen_consumed_carbon_dioxide_produced(data_frame: pd.DataFrame, name_column: str,
                                                      name_column_O2_consumed_mol: str,
                                                      name_column_CO2_produced_gas_mol: str,
                                                      carbon_dioxide_dissolved_between_time_steps_aqueous: str,
                                                      name_column_flush: str, first_row_value: float = 0
                                                      ):
        """
           Calculate the ratio of oxygen consumed to carbon dioxide produced in the DataFrame.

           Parameters:
               - data_frame (pd.DataFrame): The DataFrame to modify.
               - name_column (str): The name of the column to store the calculated ratio.
               - name_column_O2_consumed_mol (str): The name of the column containing the oxygen consumed in moles [mol]
               - name_column_CO2_produced_gas_mol (str): The name of the column containing the carbon dioxide
               produced in moles in the gas phase. [mol]
               - carbon_dioxide_dissolved_between_time_steps_aqueous (str): The name of the column containing
               the amount of carbon dioxide dissolved between time steps in the aqueous phase. [mol]
               - name_column_flush (str): The name of the column used for flushing indication.
               - first_row_value (float, optional): The value to set for the first row of the ratio column.
               Defaults to 0.

           Returns:
               None
           """
        data_frame[name_column] = data_frame[name_column_O2_consumed_mol] / \
                                  (data_frame[name_column_CO2_produced_gas_mol] +
                                   data_frame[carbon_dioxide_dissolved_between_time_steps_aqueous])

        data_frame[name_column].at[0] = first_row_value
        mask = (data_frame[name_column_flush] == 1)
        data_frame.loc[mask, name_column] = np.nan
