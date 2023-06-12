import numpy as np
import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill

from data_classes import FillType, OwnColors
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


def validate_if_there_is_a_specific_string(data_frame: pd.DataFrame, column_name: str, specific_string: [str],
                                           start_row_values_table_in_excel: int = 0) -> tuple:
    invalid_rows = []
    column_in_data_frame_to_be_checked = data_frame[column_name]
    for index in column_in_data_frame_to_be_checked.index:
        value = column_in_data_frame_to_be_checked[index]
        if  pd.isnull(value) or value not in specific_string:
            invalid_rows.append(index + start_row_values_table_in_excel)

    if len(invalid_rows) > 0:
        return column_name, invalid_rows
    else:
        return column_name, True


class validate_if_all_cells_are_correctly_filled:
    def __init__(self, dict_data_frames: {str, pd.DataFrame}):
        """

        :type dict_data_frames: {sheet name of sample, pd.DataFrame}
        """
        self.dict_data_frames = dict_data_frames
        self.sheet_names = self.dict_data_frames.keys()

        self.dict_indexes_as_panda_indexes_no_int_or_float = None
        self.dict_indexes_as_pandas_incorrect_id_parallel = None

    def fill_dict_indexes_as_panda_indexes_no_int_or_float(self, list_column_names_to_be_checked: [str],
                                                           with_feedback_true_when_column_is_oke: bool = False,
                                                           show_process: bool = False) -> {}:
        dict_indexes_as_panda_indexes_no_int_or_float = {}
        for sheet_name in self.sheet_names:
            dict_indexes_as_panda_indexes_no_int_or_float[sheet_name] = {}
            data_frame = self.dict_data_frames[sheet_name]
            for column_name in list_column_names_to_be_checked:
                indexes = validate_if_there_is_a_float_or_integer_in_cell(data_frame=data_frame,
                                                                          column_name=column_name)
                if indexes[1] is not True and not with_feedback_true_when_column_is_oke:
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

        style_color_cells_with_given_indexes(workbook=workbook,
                                             dict_sheet_name_column_names_indexes=
                                             self.dict_indexes_as_panda_indexes_no_int_or_float,
                                             header_row=header_row,
                                             color=color,
                                             fill_type=fill_type,
                                             start_row_values_table_in_excel=start_row_values_table_in_excel,
                                             show_process=show_process)

    def fill_wrong_cells_sample_id_end_parallel(self, list_column_names_to_be_checked: [str],
                                                specific_string: [str],
                                                with_feedback_true_when_column_is_oke: bool = False,
                                                show_process: bool = False ) -> {}:

        dict_indexes_as_pandas_incorrect_id_parallel = {}
        for sheet_name in self.sheet_names:
            dict_indexes_as_pandas_incorrect_id_parallel[sheet_name] = {}
            data_frame = self.dict_data_frames[sheet_name]
            for column_name in list_column_names_to_be_checked:
                indexes = validate_if_there_is_a_specific_string(data_frame=data_frame, column_name=column_name,
                                                                 specific_string=specific_string)
                if indexes[1] is not True and not with_feedback_true_when_column_is_oke:
                    dict_indexes_as_pandas_incorrect_id_parallel[sheet_name][column_name] = indexes[1]

                if show_process:
                    print(f"{sheet_name}  with column {column_name} is done")

        self.dict_indexes_as_pandas_incorrect_id_parallel = dict_indexes_as_pandas_incorrect_id_parallel

        return dict_indexes_as_pandas_incorrect_id_parallel


class ValidateInputDataStatistics:
    pass
