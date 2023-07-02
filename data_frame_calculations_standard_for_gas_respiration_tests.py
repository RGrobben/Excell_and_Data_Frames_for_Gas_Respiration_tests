import pandas as pd


class GasComposition:
    """
    A class for the gas composition.
    """

    @staticmethod
    def set_gas_composition(data_frame: pd.DataFrame,
                            ch4: float, co2: float, o2: float, n2: float,
                            name_column_ch4: str = "CH4 [%]", name_column_co2: str = "CO2 [%]",
                            name_column_o2: str = "O2 [%]", name_column_n2: str = "N2 [%]",
                            index: int = 0) -> None:
        """
            Set the values of CH4, CO2, O2, and N2 in the DataFrame.

            Parameters:
                - data_frame (pd.DataFrame): The DataFrame to modify.
                - ch4 (float): The value of CH4 in [%].
                - co2 (float): The value of CO2 in [%].
                - o2 (float): The value of O2 in [%].
                - n2 (float): The value of N2 in [%].
                - name_column_ch4 (str, optional): The name of the column for CH4. Defaults to "CH4 [%]".
                - name_column_co2 (str, optional): The name of the column for CO2. Defaults to "CO2 [%]".
                - name_column_o2 (str, optional): The name of the column for O2. Defaults to "O2 [%]".
                - name_column_n2 (str, optional): The name of the column for N2. Defaults to "N2 [%]".
                - index (int, optional): The index of the row to set the values. Defaults to 0.

            Returns:
                None

            Example:
                my_data_frame = pd.DataFrame(...)
                NicePandaFrameFunctions.set_gas_composition(data_frame=my_data_frame, ch4=10.5, co2=20.3, o2=5.7, n2=63.5)
                # The CH4, CO2, O2, and N2 values are set in the specified columns and row of the DataFrame.
            """

        data_frame.loc[index, [name_column_ch4, name_column_co2, name_column_o2, name_column_n2]] = [ch4, co2, o2, n2]

    @staticmethod
    def sum_correct_sum(data_frame: pd.DataFrame,
                        name_column_ch4: str = "CH4 [%]", name_column_co2: str = "CO2 [%]",
                        name_column_o2: str = "O2 [%]", name_column_n2: str = "N2 [%]",
                        name_column_summation: str = "Sum [%]",
                        name_column_summation_correction: str = "Sum-corr [%]",
                        name_correction_ch4: str = "CH4-corr [%]",
                        name_correction_co2: str = "CO2-corr [%]",
                        name_correction_o2: str = "O2-corr [%]",
                        name_correction_n2: str = "N2-corr [%]",
                        ) -> None:
        """
        Correct the measuring values in the DataFrame so that the sum is 100%.

        Parameters:
        - data_frame (pd.DataFrame): The DataFrame to modify.
        - name_column_ch4 (str, optional): The name of the column for CH4. Defaults to "CH4 [%]".
        - name_column_co2 (str, optional): The name of the column for CO2. Defaults to "CO2 [%]".
        - name_column_o2 (str, optional): The name of the column for O2. Defaults to "O2 [%]".
        - name_column_n2 (str, optional): The name of the column for N2. Defaults to "N2 [%]".
        - name_column_summation (str, optional): The name of the column for the summation of measuring values.
        Defaults to "Sum [%]".
        - name_column_summation_correction (str, optional): The name of the column for the corrected summation
        of measuring values. Defaults to "Sum-corr [%]".
        - name_correction_ch4 (str, optional): The name of the column for the corrected value of CH4.
        Defaults to "CH4-corr [%]".
        - name_correction_co2 (str, optional): The name of the column for the corrected value of CO2.
        Defaults to "CO2-corr [%]".
        - name_correction_o2 (str, optional): The name of the column for the corrected value of O2.
        Defaults to "O2-corr [%]".
        - name_correction_n2 (str, optional): The name of the column for the corrected value of N2.
        Defaults to "N2-corr [%]".

        Returns:
        None

        Example:
        my_data_frame = pd.DataFrame(...)
        NicePandaFrameFunctions.sum_correct_sum(data_frame=my_data_frame)
        # The measuring values are corrected so that the sum is 100% in the DataFrame.
        """
        df = data_frame

        # summation of the measuring values CH4, CO2, O2, N2 in [%]
        df[name_column_summation] = df[name_column_ch4] + df[name_column_co2] + df[name_column_o2] + df[name_column_n2]

        # Correct the measuring values so that the sum is 100%
        df[name_correction_ch4] = (100 / df[name_column_summation]) * df[name_column_ch4]
        df[name_correction_co2] = (100 / df[name_column_summation]) * df[name_column_co2]
        df[name_correction_o2] = (100 / df[name_column_summation]) * df[name_column_o2]
        df[name_correction_n2] = (100 / df[name_column_summation]) * df[name_column_n2]

        # The summation of the corrected values CH4, CO2, O2, N2. Must all be equal to 100%
        df[name_column_summation_correction] = df[name_correction_ch4] + df[name_correction_co2] + \
                                               df[name_correction_o2] + df[name_correction_n2]


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
        """
           Calculate the amount of a specific gas in moles before sampling in the DataFrame.

           Parameters:
               - data_frame (pd.DataFrame): The DataFrame to modify.
               - name_column (str): The name of the column to store the calculated amount of the specific gas in moles.
               - name_column_mg_before_or_after (str): The name of the column containing the mass of the specific gas
               (before or after sampling).
               - name_column_specific_gas_corrected (str): The name of the column containing the corrected value of the
               specific gas.

           Returns:
               None

           Example:
               my_data_frame = pd.DataFrame(...)
               NicePandaFrameFunctions.specific_gas_in_moles_before_sampling(
                   data_frame=my_data_frame,
                   name_column='Moles Before Sampling',
                   name_column_mg_before_or_after='Mass Before Sampling',
                   name_column_specific_gas_corrected='Specific Gas Corrected'
               )
               # The DataFrame now contains a new column 'Moles Before Sampling' representing the amount of a
               specific gas in moles before sampling.
           """
        data_frame[name_column] = data_frame[name_column_mg_before_or_after] * \
                                  data_frame[name_column_specific_gas_corrected] * (1 / 100)

    @staticmethod
    def carbon_total_moles(data_frame: pd.DataFrame, name_column: str, name_column_CO2: str,
                           name_column_CH4: str) -> None:
        """
          Calculate the total moles of carbon in the DataFrame.

          Parameters:
              - data_frame (pd.DataFrame): The DataFrame to modify.
              - name_column (str): The name of the column to store the calculated total moles of carbon.
              - name_column_CO2 (str): The name of the column containing the moles of CO2.
              - name_column_CH4 (str): The name of the column containing the moles of CH4.

          Returns:
              None

          Example:
              my_data_frame = pd.DataFrame(...)
              NicePandaFrameFunctions.carbon_total_moles(
                  data_frame=my_data_frame,
                  name_column='Total Moles of Carbon',
                  name_column_CO2='CO2 Moles',
                  name_column_CH4='CH4 Moles'
              )
              # The DataFrame now contains a new column 'Total Moles of Carbon' representing the total moles of carbon.
          """
        data_frame[name_column] = data_frame[name_column_CO2] + data_frame[name_column_CH4]
