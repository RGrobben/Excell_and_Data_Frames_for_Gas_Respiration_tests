from datetime import datetime

import pandas as pd
from openpyxl.styles import PatternFill

from nice_functions import NiceExcelFunction


def validate_if_there_is_a_float_or_integer_in_cell(data_frame: pd.DataFrame, column_name: str,
                                                    start_row_values_table_in_excel: int = 0) -> tuple:
    invalid_rows = []
    column_in_data_frame_to_be_checked = data_frame[column_name]
    for index in column_in_data_frame_to_be_checked.index:
        value = column_in_data_frame_to_be_checked[index]
        if not isinstance(value, (float, int)) or pd.isnull(value):
            invalid_rows.append(index + start_row_values_table_in_excel)

    if len(invalid_rows) > 0:
        return column_name, invalid_rows
    else:
        return column_name, True


def validate_if_there_is_no_specific_float_or_integer_in_cell(data_frame: pd.DataFrame, column_name: str,
                                                              specific_float_or_integer: float | int,
                                                              start_row_values_table_in_excel: int = 0) -> tuple:
    invalid_rows = []
    column_in_data_frame_to_be_checked = data_frame[column_name]
    for index in column_in_data_frame_to_be_checked.index:
        value = column_in_data_frame_to_be_checked[index]
        if not value == specific_float_or_integer or pd.isnull(value):
            invalid_rows.append(index + start_row_values_table_in_excel)

    if len(invalid_rows) > 0:
        return column_name, invalid_rows
    else:
        return column_name, True


def validate_if_there_is_a_string(data_frame: pd.DataFrame, column_name: str,
                                  start_row_values_table_in_excel: int = 0) -> tuple:
    invalid_rows = []
    column_in_data_frame_to_be_checked = data_frame[column_name]
    for index in column_in_data_frame_to_be_checked.index:
        value = column_in_data_frame_to_be_checked[index]
        if not isinstance(value, int) or pd.isnull(value):
            invalid_rows.append(index + start_row_values_table_in_excel)

    if len(invalid_rows) > 0:
        return column_name, invalid_rows
    else:
        return column_name, True


def validate_if_there_is_a_specific_string(data_frame: pd.DataFrame, column_name: str, specific_string: str,
                                           start_row_values_table_in_excel: int = 0) -> tuple:
    invalid_rows = []
    column_in_data_frame_to_be_checked = data_frame[column_name]
    for index in column_in_data_frame_to_be_checked.index:
        value = column_in_data_frame_to_be_checked[index]
        if pd.isnull(value) or value == specific_string:
            invalid_rows.append(index + start_row_values_table_in_excel)

    if len(invalid_rows) > 0:
        return column_name, invalid_rows
    else:
        return column_name, True


def validate_if_there_is_in_cell_one_of_the_specific_strings(data_frame: pd.DataFrame, column_name: str,
                                                             list_specific_string: [str],
                                                             start_row_values_table_in_excel: int = 0) -> tuple:
    invalid_rows = []
    column_in_data_frame_to_be_checked = data_frame[column_name]
    for index in column_in_data_frame_to_be_checked.index:
        value = column_in_data_frame_to_be_checked[index]
        if pd.isnull(value) or value not in list_specific_string:
            invalid_rows.append(index + start_row_values_table_in_excel)

    if len(invalid_rows) > 0:
        return column_name, invalid_rows
    else:
        return column_name, True


def check_is_string_date(string: str, date_format) -> bool:
    """
    Check if a string can be parsed as a valid date using the given format.

    Parameters:
        string (str): The string to be checked for date validity.
        date_format (str): The format of the date values. For example: "%Y-%m-%d"

    Returns:
        bool: True if the string is a valid date, False otherwise.
    """
    try:
        datetime.strptime(string, date_format)
        return True
    except ValueError:
        return False


def validate_if_in_cell_is_correct_date_or_not_filled(data_frame: pd.DataFrame, column_name_date: str,
                                                      format_date: str = "%Y-%m-%d",
                                                      start_row_values_table_in_excel: int = 0) -> tuple:
    """
        Validate the indexes of a pandas DataFrame for incorrect date values in a specific column.

        Parameters:
            data_frame (pd.DataFrame): The pandas DataFrame to be validated.
            column_name_date (str): The name of the column containing date values to be checked.
            format_date (str, optional): The format of the date values. Defaults to "%Y-%m-%d".
            start_row_values_table_in_excel (int, optional): The starting row index of the table in Excel. Defaults to 0.

        Returns:
            tuple: A tuple containing the column name and either the list of invalid row indexes or True if all rows are valid.
        """

    invalid_rows = []
    column_in_data_frame_to_be_checked = data_frame[column_name_date].astype(str)
    for index in column_in_data_frame_to_be_checked.index:
        value = column_in_data_frame_to_be_checked[index]

        if pd.isnull(value) or check_is_string_date(string=value, date_format=format_date) is False:
            invalid_rows.append(index + start_row_values_table_in_excel)

    if len(invalid_rows) > 0:
        return column_name_date, invalid_rows
    else:
        return column_name_date, True


def check_is_string_time(string: str, time_format) -> bool:
    """
    Check if a string can be parsed as a valid time using the given format.

    Parameters:
        string (str): The string to be checked for time validity.
        time_format (str): The format of the time values. For example: "%H:%M:%S"

    Returns:
        bool: True if the string is a valid time, False otherwise.
    """
    try:
        datetime.strptime(string, time_format)
        return True
    except ValueError:
        return False


def validate_if_in_cell_is_correct_time_or_not_filled(data_frame: pd.DataFrame, column_name_time: str,
                                                      format_time: str = "%H:%M:%S",
                                                      start_row_values_table_in_excel: int = 0) -> tuple:
    """
    Valideer de indexen van een pandas DataFrame op onjuiste tijdwaarden in een specifieke kolom.

    Parameters:
        data_frame (pd.DataFrame): De pandas DataFrame die moet worden gevalideerd.
        column_name_time (str): De naam van de kolom met tijdwaarden die gecontroleerd moeten worden.
        format_time (str, optioneel): Het formaat van de tijdwaarden. Standaard is "%H:%M:%S".
        start_row_values_table_in_excel (int, optioneel): De startindex van de tabel in Excel. Standaard is 0.

    Returns:
        tuple: Een tuple met de kolomnaam en ofwel de lijst met ongeldige rij-indexen of True als alle rijen geldig zijn.
    """

    invalid_rows = []
    column_in_data_frame_to_be_checked = data_frame[column_name_time].astype(str)
    for index in column_in_data_frame_to_be_checked.index:
        value = column_in_data_frame_to_be_checked[index]

        if pd.isnull(value) or check_is_string_time(string=value, time_format=format_time) is False:
            invalid_rows.append(index + start_row_values_table_in_excel)

    if len(invalid_rows) > 0:
        return column_name_time, invalid_rows
    else:
        return column_name_time, True


def style_color_cells_with_given_indexes(workbook, dict_sheet_name_column_names_indexes: {},
                                         header_row: int,
                                         color: str, fill_type: str,
                                         start_row_values_table_in_excel: int = 1,
                                         show_process: bool = False) -> None:
    """

    :param show_process: when you like to see the process.
    :param workbook: The workbook
    :param dict_sheet_name_column_names_indexes: {sheet_name: {column_name: indexes}}
    :param header_row: the row where the header is.
    :param color: the colorcode based on RGB colors
    :param fill_type: Fill type: "solid", "gradient", "patter", "None"
    :param start_row_values_table_in_excel: the starting row of the values of the table in Excel. In Excel the rows
    are starting with 1.
    """
    color_fill = PatternFill(start_color=color, end_color=color, fill_type=fill_type)

    for sheet_name, sheet_data in dict_sheet_name_column_names_indexes.items():
        sheet = workbook[sheet_name]
        if show_process is True:
            print(f"started with {sheet_name}")
        for column_name, indexes in sheet_data.items():
            column_letter = NiceExcelFunction.find_column_name_excel_index_based_on_column_name_string_in_given_row(
                workbook=workbook, sheet_name=sheet_name, search_string=column_name, header_row=header_row)
            for index in indexes:
                index_row_in_excel = start_row_values_table_in_excel + index
                column_and_row_excel_combination = column_letter + str(index_row_in_excel)
                sheet[column_and_row_excel_combination].fill = color_fill


class validate_if_all_cells_are_correctly_filled:
    def __init__(self, dict_data_frames: {str, pd.DataFrame}):
        """

        :type dict_data_frames: {sheet name of sample, pd.DataFrame}
        """
        self.dict_data_frames = dict_data_frames
        self.sheet_names = self.dict_data_frames.keys()

        self.dict_indexes_as_panda_indexes_no_int_or_float = None

        self.dict_indexes_as_pandas_incorrect_sample_id = None
        self.dict_indexes_as_pandas_incorrect_parallel = None
        self.dict_indexes_as_pandas_incorrect_gc_method = None
        self.list_no_correct_strings_and_parallel = []

        self.dict_indexes_as_pandas_no_weight_when_flush = None
        self.dict_indexes_as_pandas_incorrect_date = None

    def fill_dict_indexes_as_panda_indexes_no_int_or_float(self, list_column_names_to_be_checked: [str],
                                                           show_process: bool = False) -> {}:
        dict_indexes_as_panda_indexes_no_int_or_float = {}
        for sheet_name in self.sheet_names:
            dict_indexes_as_panda_indexes_no_int_or_float[sheet_name] = {}
            data_frame = self.dict_data_frames[sheet_name]
            for column_name in list_column_names_to_be_checked:
                indexes = validate_if_there_is_a_float_or_integer_in_cell(data_frame=data_frame,
                                                                          column_name=column_name)
                if indexes[1] is not True:
                    dict_indexes_as_panda_indexes_no_int_or_float[sheet_name][column_name] = indexes[1]

                if show_process:
                    print(f"{sheet_name}  with column {column_name} is done")

        self.dict_indexes_as_panda_indexes_no_int_or_float = dict_indexes_as_panda_indexes_no_int_or_float

        return dict_indexes_as_panda_indexes_no_int_or_float

    def fill_wrong_cells_in_excel_no_int_or_float(self, workbook, header_row: int,
                                                  start_row_values_table_in_excel: int,
                                                  color: str = "FFFF00",
                                                  fill_type: str = "solid",
                                                  show_process: bool = False):
        # "FFFF00" is the color code for yellow
        style_color_cells_with_given_indexes(workbook=workbook,
                                             dict_sheet_name_column_names_indexes=
                                             self.dict_indexes_as_panda_indexes_no_int_or_float,
                                             header_row=header_row,
                                             color=color,
                                             fill_type=fill_type,
                                             start_row_values_table_in_excel=start_row_values_table_in_excel,
                                             show_process=show_process)

    def fill_dict_indexes_as_pandas_incorrect_sample_id(self, column_name_to_be_checked: str,
                                                        list_specific_string: [str],
                                                        show_process: bool = False) -> {}:

        dict_indexes_as_pandas_incorrect_sample_id = {}
        for sheet_name, specific_string in zip(self.sheet_names, list_specific_string):
            dict_indexes_as_pandas_incorrect_sample_id[sheet_name] = {}
            data_frame = self.dict_data_frames[sheet_name]
            indexes = validate_if_there_is_a_specific_string(data_frame=data_frame,
                                                             column_name=column_name_to_be_checked,
                                                             specific_string=specific_string)
            if indexes[1] is not True:
                dict_indexes_as_pandas_incorrect_sample_id[sheet_name][column_name_to_be_checked] = indexes[1]
            if show_process:
                print(f"{sheet_name}  with column {column_name_to_be_checked} is done")

        self.dict_indexes_as_pandas_incorrect_sample_id = dict_indexes_as_pandas_incorrect_sample_id
        self.list_no_correct_strings_and_parallel.append(dict_indexes_as_pandas_incorrect_sample_id)

        return dict_indexes_as_pandas_incorrect_sample_id

    def fill_dict_indexes_as_pandas_incorrect_parallel(self, column_name_to_be_checked: str,
                                                       list_specific_float_or_integer: [int],
                                                       show_process: bool = False) -> {}:

        dict_indexes_as_pandas_incorrect_parallel = {}
        for sheet_name, specific_integer in zip(self.sheet_names, list_specific_float_or_integer):
            dict_indexes_as_pandas_incorrect_parallel[sheet_name] = {}
            data_frame = self.dict_data_frames[sheet_name]
            indexes = validate_if_there_is_no_specific_float_or_integer_in_cell(data_frame=data_frame,
                                                                                column_name=column_name_to_be_checked,
                                                                                specific_float_or_integer=
                                                                                specific_integer)
            if indexes[1] is not True:
                dict_indexes_as_pandas_incorrect_parallel[sheet_name][column_name_to_be_checked] = indexes[1]
            if show_process:
                print(f"{sheet_name}  with column {column_name_to_be_checked} is done")

        self.dict_indexes_as_pandas_incorrect_parallel = dict_indexes_as_pandas_incorrect_parallel
        self.list_no_correct_strings_and_parallel.append(dict_indexes_as_pandas_incorrect_parallel)

        return dict_indexes_as_pandas_incorrect_parallel

    def fill_dict_indexes_as_pandas_incorrect_gc_method(self, column_name_to_be_checked: str,
                                                        list_specific_string: [str] = None,
                                                        show_process: bool = False):
        """
        This functions returns a dictionary and fills the dictionary in the class with indexes of incorrect filled cells
        for the GC.

        :param column_name_to_be_checked: the name of the column that must be checked and represents the GC method column
        :param list_specific_string: here can you specify the specific strings which are correct.
                The default is set on: "LM" for Low method, "HM" for High Method, "VHM" for Very High Method
        :param show_process: when set on True than the function shows the process.
        :return:
        """
        if list_specific_string is None:
            list_specific_string = ["LM", "HM", "VHM"]
        dict_indexes_as_pandas_incorrect_gc_method = {}
        for sheet_name in self.sheet_names:
            dict_indexes_as_pandas_incorrect_gc_method[sheet_name] = {}
            data_frame = self.dict_data_frames[sheet_name]
            indexes = validate_if_there_is_in_cell_one_of_the_specific_strings(data_frame=data_frame,
                                                                               column_name=column_name_to_be_checked,
                                                                               list_specific_string=list_specific_string)
            if indexes[1] is not True:
                dict_indexes_as_pandas_incorrect_gc_method[sheet_name][column_name_to_be_checked] = indexes[1]
            if show_process:
                print(f"{sheet_name}  with column {column_name_to_be_checked} is done")

        self.dict_indexes_as_pandas_incorrect_gc_method = dict_indexes_as_pandas_incorrect_gc_method
        self.list_no_correct_strings_and_parallel.append(dict_indexes_as_pandas_incorrect_gc_method)

        return dict_indexes_as_pandas_incorrect_gc_method

    def fill_wrong_cells_in_excel_no_or_no_specific_string_or_wrong_parallel(self, workbook, header_row: int,
                                                                             start_row_values_table_in_excel: int,
                                                                             color: str = "FF9933",
                                                                             fill_type: str = "solid",
                                                                             show_process: bool = False):

        # this is the RGB color code for orange "FF9933"
        for dict_indexes in self.list_no_correct_strings_and_parallel:
            print(dict_indexes)
            if dict_indexes is None:
                continue
            else:
                style_color_cells_with_given_indexes(workbook=workbook,
                                                     dict_sheet_name_column_names_indexes=dict_indexes,
                                                     header_row=header_row,
                                                     color=color,
                                                     fill_type=fill_type,
                                                     start_row_values_table_in_excel=start_row_values_table_in_excel,
                                                     show_process=show_process)

    def fill_dict_indexes_as_pandas_no_weight_when_flush(self, column_name_to_be_checked: str,
                                                         column_name_flush: str,
                                                         show_process: bool = False) -> {}:
        dict_indexes_as_pandas_no_weight_when_flush = {}
        for sheet_name in self.sheet_names:
            dict_indexes_as_pandas_no_weight_when_flush[sheet_name] = {}
            data_frame = self.dict_data_frames[sheet_name]
            invalid_rows = []
            column_in_data_frame_to_be_checked = data_frame[column_name_to_be_checked]
            column_in_data_frame_flush = data_frame[column_name_flush]
            for index in column_in_data_frame_to_be_checked.index:
                if column_in_data_frame_flush[index] == 1:
                    value = column_in_data_frame_to_be_checked[index]
                    if not isinstance(value, (float, int)) or pd.isnull(value):
                        invalid_rows.append(index)

            if len(invalid_rows) > 0:
                dict_indexes_as_pandas_no_weight_when_flush[sheet_name][column_name_to_be_checked] = invalid_rows

            if show_process:
                print(f"{sheet_name}  with column {column_name_to_be_checked} is done")

        self.dict_indexes_as_pandas_no_weight_when_flush = dict_indexes_as_pandas_no_weight_when_flush

        return dict_indexes_as_pandas_no_weight_when_flush

    def fill_wrong_cells_in_excel_no_weight_when_flush(self, workbook, header_row: int,
                                                       start_row_values_table_in_excel: int,
                                                       color: str = "FFFF00",
                                                       fill_type: str = "solid",
                                                       show_process: bool = False):
        # "FFFF00" is the color code for yellow
        style_color_cells_with_given_indexes(workbook=workbook,
                                             dict_sheet_name_column_names_indexes=
                                             self.dict_indexes_as_pandas_no_weight_when_flush,
                                             header_row=header_row,
                                             color=color,
                                             fill_type=fill_type,
                                             start_row_values_table_in_excel=start_row_values_table_in_excel,
                                             show_process=show_process)

    def fill_dict_indexes_as_pandas_incorrect_date(self, column_name_date: str, format_date: str = "%Y-%m-%d",
                                                   show_process: bool = False) -> {}:

        dict_indexes_as_pandas_incorrect_date = {}
        for sheet_name in self.sheet_names:
            dict_indexes_as_pandas_incorrect_date[sheet_name] = {}
            data_frame = self.dict_data_frames[sheet_name]

            indexes = validate_if_in_cell_is_correct_date_or_not_filled(data_frame=data_frame,
                                                                        column_name_date=column_name_date,
                                                                        format_date=format_date)
            if indexes[1] is not True:
                dict_indexes_as_pandas_incorrect_date[sheet_name][column_name_date] = indexes[1]

            if show_process:
                print(f"{sheet_name}  with column {column_name_date} is done")

        self.dict_indexes_as_pandas_incorrect_date = dict_indexes_as_pandas_incorrect_date

        return dict_indexes_as_pandas_incorrect_date


    def time(self):
        pass

    def fill_no_correct_date_time(self):
        pass

    def the_are_constants_filled(self):
        pass

    def fil_missing_constants(self):
        pass


# TODO: write unit tests!
class ValidateInputDataStatistics:
    pass

    def outliers(self):
        pass

    def fill_outliers(self):
        pass
