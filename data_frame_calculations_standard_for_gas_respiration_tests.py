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
