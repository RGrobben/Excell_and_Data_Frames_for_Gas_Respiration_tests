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
    :param color: the color from the Color class.
    :param fill_type: Fill type from the FillType class
    :param start_row_values_table_in_excel: the starting row of the values of the table in Excel. In Excel the rows
    are starting with 1.
    """
    color_fill = PatternFill(start_color=color, end_color=color, fill_type=fill_type)

    for sheet_name, sheet_data in dict_sheet_name_column_names_indexes.items():
        sheet = workbook[sheet_name]
        if show_process is True:
            print(f"started with {sheet_name}")
        for column_name, indexes in sheet_data.items():
            print(column_name)
            column_letter = NiceExcelFunction.find_column_name_excel_index_based_on_column_name_string_in_given_row(
                workbook=workbook, sheet_name=sheet_name, search_string=column_name, header_row=header_row)
            print(column_letter)
            for index in indexes:
                index_row_in_excel = start_row_values_table_in_excel + index
                column_and_row_excel_combination = column_letter + str(index_row_in_excel)
                sheet[column_and_row_excel_combination].fill = color_fill
            if show_process is True:
                print(f"{column_name} is done")


class validate_if_all_cells_are_correctly_filled:
    def __init__(self, dict_data_frames: {str, pd.DataFrame}):
        """

        :type dict_data_frames: {sheet name of sample, pd.DataFrame}
        """
        self.dict_data_frames = dict_data_frames
        self.sheet_names = self.dict_data_frames.keys

    def fill_dict_indexes_in_panda_no_int_or_float(self, list_column_names_to_be_checked: [str],
                                                   with_feedback_when_column_is_oke: bool = False,
                                                   show_process: bool = False):
        dict_indexes_in_panda_no_int_or_float = {}
        for sheet_name in self.sheet_names:
            data_frame = self.dict_data_frames[sheet_name]
            for column_name in list_column_names_to_be_checked:
                indexes = validate_if_there_is_a_float_or_integer_in_cell(data_frame=data_frame,
                                                                          column_name=column_name)
                if indexes[1] is not True and not with_feedback_when_column_is_oke:
                    dict_indexes_in_panda_no_int_or_float[sheet_name][column_name] = indexes[1]

                if show_process:
                    print(f"{sheet_name}  with column {column_name} is done")



class ValidateInputData:
    def __init__(self, data_frame: pd.DataFrame):
        self.data_frame = data_frame

    def validate_if_there_are_dates(self, column_name_date: str):
        # if column_name_date not in self.data_frame.columns:
        #     return f"Column '{column_name_date}' does not exist in the data frame."
        #
        # self.data_frame[column_name_date] = pd.to_datetime(self.data_frame[column_name_date].astype(str), dayfirst=False)
        #
        # mask = self.data_frame[column_name_date].apply(lambda x: isinstance(x, datetime))
        # if mask.all(True):
        #     return True
        # else:
        #     # valse_indexes = []
        #     # for mask_value in mask:
        #     #     if not True:
        #     #         valse_indexes.append(mask.)
        #     # return valse_indexes
        #     return mask[~mask].index.tolist()
        pass

    def validate_if_there_are_times(self):
        pass

    def validate_if_time_plus_date_is_chronologically(self):
        pass

    def validate_if_there_are_P_atmosphere(self, name_column_p_atmosphere: str):
        validate_if_there_is_a_float_or_integer_in_cell(data_frame=self.data_frame,
                                                        column_name=name_column_p_atmosphere)

    def validate_if_there_are_P_before(self):
        pass

    def validate_if_there_are_P_after(self):
        pass

    def validate_if_there_are_ch4(self):
        pass

    def validate_if_there_are_co2(self):
        pass

    def validate_if_there_are_o2(self):
        pass

    def validate_if_there_are_n2(self):
        pass

    def validate_if_there_are_flush(self):
        pass

    def validate_type_gc_method(self):
        pass

    def validate_if_there_is_weight_with_flush(self):
        pass


class ValidateInputDataStatistics:
    pass
