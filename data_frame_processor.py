import pandas as pd
import datetime
from typing import Any, Optional

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
    def add_day_column(data_frame: pd.DataFrame, date_column_name: str, time_column_name: str,
                       day_column_name: Optional[str] = 'Day', fraction_to_time: bool = False) -> None:
        """
        Add a "Day" column to the DataFrame using the specified date and time columns.

        :param data_frame:
        :param date_column_name: The name of the date column.
        :param time_column_name: The name of the time column.
        :param day_column_name: The name for the new "Day" column. Defaults to 'Day'.\
        """

        # def formula_fraction_to_time(fraction):
        #     total_seconds = fraction * 24 * 60 * 60
        #     return str(datetime.timedelta(seconds=total_seconds))
        #
        # # Convert fraction of time into time
        # if fraction_to_time:
        #     data_frame[time_column_name] = data_frame[time_column_name].apply(formula_fraction_to_time)
        #
        # # Convert date column to datetime using the "day / month / year" format
        # data_frame[date_column_name] = pd.to_datetime(data_frame[date_column_name], format='%d/%m/%Y')
        #
        # # Convert time column to string
        # data_frame[time_column_name] = data_frame[time_column_name].astype(str)
        #
        # # # creating "Day" column with the "Date" + "Time" columns
        # # data_frame[day_column_name] = pd.to_datetime(
        # #     data_frame[date_column_name].astype(str) + ' ' + data_frame[time_column_name].astype(str))
        #
        # # Creating "Day" column with the "Date" + "Time" columns
        # data_frame[day_column_name] = pd.to_datetime(
        #     data_frame[date_column_name].dt.strftime('%Y-%m-%d') + ' ' + data_frame[time_column_name])
        #
        # # Set the "Day" column with the start point at the first row. So row zero is day zero
        # data_frame[day_column_name] = data_frame[day_column_name] - data_frame.at[0, day_column_name]

        def formula_fraction_to_time(fraction):
            total_seconds = fraction * 24 * 60 * 60
            return str(datetime.timedelta(seconds=total_seconds))

        # Convert fraction of time into time
        if fraction_to_time:
            data_frame[time_column_name] = data_frame[time_column_name].apply(formula_fraction_to_time)

        # Convert date column to datetime using the "day / month / year" format
        data_frame[date_column_name] = pd.to_datetime(data_frame[date_column_name], format='%d/%m/%Y')

        # Convert time column to string
        data_frame[time_column_name] = data_frame[time_column_name].astype(str)

        # Creating "Day" column with the "Date" + "Time" columns
        data_frame[day_column_name] = pd.to_datetime(
            data_frame[date_column_name].dt.strftime('%Y-%m-%d') + ' ' + data_frame[time_column_name])

        # Set the "Day" column with the start point at the first row. So row zero is day zero
        data_frame[day_column_name] = data_frame[day_column_name] - data_frame.at[0, day_column_name]

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
