import pandas as pd
from typing import Any,

from IPython.display import display


class DataFrameProcessor:
    """
    A class for processing pandas DataFrames standard calculations.
    """

    @staticmethod
    def fill_nan_values(data_frame: pd.DataFrame, column_name: str, value: Any) -> None:
        """
        Fill the NaN values in a column with a specified value.

        :param data_frame:
        :param column_name: The name of the column to fill NaN values.
        :param value: The value to fill NaN values.
        """
        data_frame[column_name] = data_frame[column_name].fillna(value)

    @staticmethod
    def add_day_column(data_frame: pd.DataFrame, date_column_name: str,
                       time_column_name: str, day_plus_time_column_name: str = "Day + Time",
                       day_column_name: str = "Day", dayfirst: bool = False) -> None:

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
        Replaces a column in a the DataFrame at the left of the location of column that is named as the desired location.

        Args:
        - name_replaced_column: The name of the column to be replaced.
        - name_column_of_position: The name of the column where the replaced column should be positioned.

        Returns:
        - None
        """
        column_to_be_replaced = data_frame.pop(name_replaced_column)
        data_frame.insert(loc=data_frame.columns.get_loc(name_column_of_position),
                          column=name_replaced_column, value=column_to_be_replaced)
