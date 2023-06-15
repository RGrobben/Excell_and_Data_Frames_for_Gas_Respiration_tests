import pandas as pd
from openpyxl.workbook import Workbook

from data_classes import ConstantsSample
from nice_functions import NiceExcelFunction
from validation_input_data.general_validation_functions import validate_if_there_is_a_float_or_integer_in_cell, \
    validate_if_there_is_no_specific_float_or_integer_in_cell, validate_if_there_is_a_specific_string, \
    validate_if_there_is_in_cell_one_of_the_specific_strings, validate_if_in_cell_is_correct_date_or_not_filled, \
    validate_if_in_cell_is_correct_time_or_not_filled, style_color_cells_with_given_indexes


class validate_if_all_cells_are_correctly_filled:
    def __init__(self, dict_data_frames: {str, pd.DataFrame}, dict_constants_data_classes: {str, ConstantsSample}):
        """

        :type dict_data_frames: {sheet name of sample, pd.DataFrame}
        """
        self.dict_data_frames = dict_data_frames
        self.sheet_names = self.dict_data_frames.keys()
        self.dict_constants_data_classes = dict_constants_data_classes

        self.dict_indexes_as_panda_indexes_no_int_or_float = None

        self.dict_indexes_as_pandas_incorrect_sample_id = None
        self.dict_indexes_as_pandas_incorrect_parallel = None
        self.dict_indexes_as_pandas_incorrect_gc_method = None
        self.list_no_correct_strings_and_parallel = []

        self.dict_indexes_as_pandas_no_weight_when_flush = None
        self.dict_indexes_as_pandas_incorrect_date = None
        self.dict_indexes_as_pandas_incorrect_time = None

        self.dict_wrong_constants_for_each_sheet_name = None

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

    def fill_dict_indexes_as_pandas_incorrect_time(self, column_name_time: str, format_time: str = "%H:%M:%S",
                                                   show_process: bool = False) -> {}:

        dict_indexes_as_pandas_incorrect_time = {}
        for sheet_name in self.sheet_names:
            dict_indexes_as_pandas_incorrect_time[sheet_name] = {}
            data_frame = self.dict_data_frames[sheet_name]

            indexes = validate_if_in_cell_is_correct_time_or_not_filled(data_frame=data_frame,
                                                                        column_name_time=column_name_time,
                                                                        format_time=format_time)
            if indexes[1] is not True:
                dict_indexes_as_pandas_incorrect_time[sheet_name][column_name_time] = indexes[1]

            if show_process:
                print(f"{sheet_name}  with column {column_name_time} is done")

        self.dict_indexes_as_pandas_incorrect_time = dict_indexes_as_pandas_incorrect_time

        return dict_indexes_as_pandas_incorrect_time

    def fill_wrong_cells_no_correct_date_and_time(self,
                                                  workbook, header_row: int,
                                                  start_row_values_table_in_excel: int,
                                                  color: str = "FF6666",
                                                  fill_type: str = "solid",
                                                  show_process: bool = False):

        # "FF6666" is the color code for light red
        for dictionary in self.dict_indexes_as_pandas_incorrect_time, self.dict_indexes_as_pandas_incorrect_date:
            style_color_cells_with_given_indexes(workbook=workbook,
                                                 dict_sheet_name_column_names_indexes=dictionary,
                                                 header_row=header_row,
                                                 color=color,
                                                 fill_type=fill_type,
                                                 start_row_values_table_in_excel=start_row_values_table_in_excel,
                                                 show_process=show_process)

    def fill_dict_with_indexes_as_excel_when_constants_is_incorrect(self,
                                                                    start_row_in_excel: int,
                                                                    workbook: Workbook,
                                                                    start_row_constants_value: int,
                                                                    end_row_constants_value: int,
                                                                    column_letter_values):

        dict_wrong_constants_for_each_sheet_name = {}

        start_col_values = NiceExcelFunction.get_column_index_from_letter(column_letter_values)
        end_col_values = start_col_values + 1
        for sheet_name in workbook.sheetnames:
            indexes = []
            sheet = workbook[sheet_name]
            values_list = list(sheet.iter_rows(min_row=start_row_constants_value,
                                               min_col=start_col_values,
                                               max_row=end_row_constants_value,
                                               max_col=end_col_values,
                                               values_only=True))

            for index, value in enumerate(values_list):
                if not isinstance(value, float):
                    indexes.append(index + start_row_in_excel)

            if len(indexes) > 0:
                dict_wrong_constants_for_each_sheet_name[sheet_name] = indexes

        self.dict_wrong_constants_for_each_sheet_name = dict_wrong_constants_for_each_sheet_name

        return dict_wrong_constants_for_each_sheet_name

    def fil_wrong_cells_constants_missing_constants(self, workbook, header_row: int,
                                                    color: str = "FF6666",
                                                    fill_type: str = "solid",
                                                    show_process: bool = False):

        # "FF6666" is the color code for light red
        style_color_cells_with_given_indexes(workbook=workbook,
                                             dict_sheet_name_column_names_indexes=
                                             self.dict_wrong_constants_for_each_sheet_name,
                                             header_row=header_row,
                                             color=color,
                                             fill_type=fill_type,
                                             start_row_values_table_in_excel=0,
                                             show_process=show_process)


# TODO: write unit tests!
class ValidateInputDataStatistics:
    pass

    def outliers(self):
        pass

    def fill_outliers(self):
        pass
