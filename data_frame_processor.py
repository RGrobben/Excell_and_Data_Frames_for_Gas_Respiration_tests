import pandas as pd
from typing import Any


class DataFrameProcessor:
    """
    A class for processing pandas DataFrames with standard operations.
    """

    @staticmethod
    def fill_nan_values(data_frame: pd.DataFrame, column_name: str, value: float) -> None:
        """
        Fill the NaN values in a column with a specified value.

        Parameters:
            - data_frame (pd.DataFrame): The DataFrame to modify.
            - column_name (str): The name of the column to fill NaN values.
            - value (float): The value to fill NaN values.

        Returns:
            None
        """
        data_frame[column_name] = data_frame[column_name].fillna(value)

    @staticmethod
    def add_day_column(data_frame: pd.DataFrame, date_column_name: str,
                       time_column_name: str, day_plus_time_column_name: str = "Day + Time",
                       day_column_name: str = "Day", dayfirst: bool = False) -> None:
        """
            Add a new column to the DataFrame representing the number of days since the first row's date and time.

            Parameters:
                - data_frame (pd.DataFrame): The DataFrame to modify.
                - date_column_name (str): The name of the column containing the date values.
                - time_column_name (str): The name of the column containing the time values.
                - day_plus_time_column_name (str, optional): The name of the new column combining date and time values. Defaults to "Day + Time".
                - day_column_name (str, optional): The name of the new column representing the number of days. Defaults to "Day".
                - dayfirst (bool, optional): Whether the date format is day first (e.g., "25-12-2022" for December 25th, 2022). Defaults to False.

            Returns:
                None

            Note:
                - The method converts the date and time columns to string format.
                - It combines the date and time values into a new column named "Day + Time" using the pd.to_datetime() function.
                - It calculates the number of days since the first row's date and time and assigns the values to a new column named "Day".
                - The calculation is based on the difference between each row's "Day + Time" value and the first row's "Day + Time" value.
            """
        data_frame[date_column_name] = data_frame[date_column_name].astype(str)
        data_frame[time_column_name] = data_frame[time_column_name].astype(str)

        data_frame[day_plus_time_column_name] = pd.to_datetime(data_frame[date_column_name] + ' ' +
                                                               data_frame[time_column_name], dayfirst=dayfirst)

        data_frame[day_column_name] = (data_frame[day_plus_time_column_name] -
                                       data_frame[day_plus_time_column_name].iloc[0]) / pd.Timedelta(days=1)

    @staticmethod
    def replace_position_column(data_frame: pd.DataFrame, name_replaced_column: str,
                                name_column_of_position: str) -> None:
        """
        Replaces a column in the DataFrame at the left of the location of the column named as the desired location.

        Parameters:
        - data_frame (pd.DataFrame): The DataFrame to modify.
        - name_replaced_column (str): The name of the column to be replaced.
        - name_column_of_position (str): The name of the column where the replaced column should be positioned.

        Returns:
        None
        """
        column_to_be_replaced = data_frame.pop(name_replaced_column)
        data_frame.insert(loc=data_frame.columns.get_loc(name_column_of_position),
                          column=name_replaced_column, value=column_to_be_replaced)
