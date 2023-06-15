import dataclasses
import os
import shutil
from datetime import datetime
from typing import List

import pandas as pd
from openpyxl.reader.excel import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.workbook import Workbook

from data_classes import ConstantsSample


class ExcelManager:
    """A class for managing an Excel file."""

    def __init__(self, file_path: str) -> None:
        """
        Initialize the ExcelManager.

        Args:
            file_path (str): The path to the Excel file.
        """
        self.file_path = file_path
        self.workbook_values = None
        self.workbook_formula = None
        self.dict_panda_data_frames = {}
        self.dict_constants_data_frames = {}
        self.dict_constants_data_classes = {}
        self.sheet_names = {}

    def load_workbook(self) -> None:
        """Load the Excel file as a workbook."""
        self.workbook_values = load_workbook(filename=self.file_path, data_only=True)
        self.workbook_formula = load_workbook(filename=self.file_path)

    def get_sheet_names(self) -> List[str]:
        """
        Get the names of all sheets in the workbook.

        Returns:
            List[str]: A list of sheet names.
        """
        if not self.workbook_values:
            raise Exception("Workbook is not loaded.")
        return self.workbook_values.sheetnames

    def load_sheet_table(
            self,
            sheet_name: str,
            start_row: int,
            start_column: int = None,
            end_row: int = None,
            end_column: int = None,
            values_only: bool = True,
            data_only: bool = False
    ):
        """
            Load a portion of an Excel sheet as a pandas DataFrame.

            Parameters
            ----------
            sheet_name : str
                The name of the sheet to load.
            start_row : int
                The first row of the range to load.
            start_column : int, optional
                The first column of the range to load. If None, starts from the first column.
            end_row : int, optional
                The last row of the range to load. If None, loads until the last row.
            end_column : int, optional
                The last column of the range to load. If None, loads until the last column.

            Raises
            ------
            Exception
                If the workbook has not been loaded.

            Returns
            -------
            pd.DataFrame
                The loaded data as a pandas DataFrame, with the first row of the loaded range as headers.
                :param sheet_name:
                :param start_row:
                :param start_column:
                :param end_row:
                :return:
                :param end_column:
                :param data_only:
                :param values_only:
            """

        if data_only is not None:
            workbook = self.workbook_values
        else:
            workbook = self.workbook_formula

        if not workbook:
            raise Exception("Workbook is not loaded.")

        sheet = workbook[sheet_name]

        data = list(sheet.iter_rows(min_row=start_row,
                                    min_col=start_column,
                                    max_row=end_row,
                                    max_col=end_column,
                                    values_only=values_only))

        header = data[0]
        values = data[1:]
        data_frame = pd.DataFrame(data=values, columns=header)

        return data_frame

    def load_sheet_table_with_input_header(
            self,
            sheet_name: str,
            start_row: int,
            column_names: [str],
            start_column: int = None,
            end_row: int = None,
            end_column: int = None,
            values_only: bool = True,
            data_only: bool = False
    ):
        """
            Load a portion of an Excel sheet as a pandas DataFrame.

            Parameters
            ----------
            sheet_name : str
                The name of the sheet to load.
            start_row : int
                The first row of the range to load.
            start_column : int, optional
                The first column of the range to load. If None, starts from the first column.
            end_row : int, optional
                The last row of the range to load. If None, loads until the last row.
            end_column : int, optional
                The last column of the range to load. If None, loads until the last column.

            Raises
            ------
            Exception
                If the workbook has not been loaded.

            Returns
            -------
            pd.DataFrame
                The loaded data as a pandas DataFrame, with the first row of the loaded range as headers.
                :param column_names:
                :param sheet_name:
                :param start_row:
                :param start_column:
                :param end_row:
                :return:
                :param end_column:
                :param data_only:
                :param values_only:
            """

        if data_only is not None:
            workbook = self.workbook_values
        else:
            workbook = self.workbook_formula

        if not workbook:
            raise Exception("Workbook is not loaded.")

        sheet = workbook[sheet_name]

        data = list(sheet.iter_rows(min_row=start_row,
                                    min_col=start_column,
                                    max_row=end_row,
                                    max_col=end_column,
                                    values_only=values_only))

        values = data[1:]
        data_frame = pd.DataFrame(data=values, columns=column_names)

        return data_frame

    def load_constants_as_data_frame(
            self,
            sheet_name: str,
            start_row: int,
            start_col: int,
            end_row: int = None,
            values_only: bool = True,
            data_only: bool = False
    ):
        if data_only:
            workbook = self.workbook_values
        else:
            workbook = self.workbook_formula

        if not workbook:
            raise Exception("Workbook is not loaded.")

        sheet = workbook[sheet_name]

        end_col = start_col + 1

        data = list(sheet.iter_rows(min_row=start_row,
                                    min_col=start_col,
                                    max_row=end_row,
                                    max_col=end_col,
                                    values_only=values_only))

        # Create a dictionary to hold the constant names and values
        constants_dict = {row[0]: row[1] for row in data}

        # Create a DataFrame using this dictionary
        data_frame = pd.DataFrame(constants_dict, index=[0])

        return data_frame

    def load_constants_as_data_class(
            self,
            sheet_name: str,
            start_row: int,
            start_col: int,
            end_row: int = None,
            values_only: bool = True,
            data_only: bool = False
    ):
        if data_only:
            workbook = self.workbook_values
        else:
            workbook = self.workbook_formula

        if not workbook:
            raise Exception("Workbook is not loaded.")

        sheet = workbook[sheet_name]

        end_col = start_col + 1

        data = list(sheet.iter_rows(min_row=start_row,
                                    min_col=start_col,
                                    max_row=end_row,
                                    max_col=end_col,
                                    values_only=values_only))

        # Create a dictionary to hold the constant names and values
        constants_dict = {row[0]: row[1] for row in data}

        # Instantiate the data class
        data_class_instance = ConstantsSample

        # Assign the constants to the data class fields
        for field in dataclasses.fields(data_class_instance):
            if field.name in constants_dict:
                setattr(data_class_instance, field.name, constants_dict[field.name])

        return data_class_instance

    @staticmethod
    def replace_table_in_specific_sheet_with_data_frame(
            excel_file_path: str,
            sheet_name: str,
            start_row: int,
            header: bool,
            data_frame: pd.DataFrame,
            start_column: int = 1,

    ) -> None:
        if not excel_file_path:
            raise Exception("there is no excel_file with that path")

        workbook = load_workbook(filename=excel_file_path)
        sheet = workbook[sheet_name]

        # change the data frame in to rows. Without index and headers, just only the data.
        rows = dataframe_to_rows(data_frame, index=False, header=header)

        # remove the existing table
        for row in sheet.iter_rows(min_row=start_row, min_col=start_column):
            for cell in row:
                cell.value = None

        # write the new data frame to the worksheet
        for r_idx, row in enumerate(rows):
            for c_idx, value in enumerate(row):
                sheet.cell(row=r_idx + start_row, column=c_idx + start_column, value=value)

        # save copy
        workbook.save(excel_file_path)

    # TODO: does not work yet
    @staticmethod
    def make_copy_of_excel(
            excel_path_to_copy: str,
            output_dir: str,
            output_name: str = "output"
    ):

        # make new path for copy
        # generate a unique filename based on the current date and time
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        output_name = f"{output_name}_{timestamp}.xlsx"

        # create the full file path
        output_path = output_dir + '\\' + output_name

        # make copy of excell file
        shutil.copy(excel_path_to_copy, output_path)

    def fill_dict_panda_data_frames(self,
                                    data_frame: pd.DataFrame,
                                    sheets: list[str],
                                    print_process: False | True = False,
                                    ) -> None:

        sheet_names = sheets

        for sheet_name in sheet_names:
            self.dict_panda_data_frames[sheet_name] = data_frame

            if print_process is not False:
                print(f'Show process: {sheet_name} is done')

    def get_dict_panda_data_frames(self) -> {str, pd.DataFrame}:
        return self.dict_panda_data_frames

    def fill_dict_constants_data_frames(self,
                                        data_frame: pd.DataFrame,
                                        sheets: list[str],
                                        print_process: False | True = False,
                                        ) -> None:

        sheet_names = sheets

        for sheet_name in sheet_names:
            self.dict_constants_data_frames[sheet_name] = data_frame

            if print_process is not False:
                print(f'Show process: {sheet_name} is done')

    def get_dict_constants_data_frames(self) -> {str, pd.DataFrame}:
        return self.dict_constants_data_frames

    def fill_dict_constants_data_classes(self,
                                         data_class: ConstantsSample,
                                         sheets: list[str],
                                         print_process: False | True = False,
                                         ) -> None:
        sheet_names = sheets

        for sheet_name in sheet_names:
            self.dict_constants_data_classes[sheet_name] = data_class

            if print_process is not False:
                print(f'Show process: {sheet_name} is done')

    def get_dict_constants_data_classes(self) -> {str, ConstantsSample}:
        return self.dict_constants_data_classes

    def create_new_workbook(self, data_only: bool = False, **kwargs) -> Workbook:
        return load_workbook(filename=self.file_path, data_only=data_only, **kwargs)

    @staticmethod
    def make_excel_based_on_workbook(workbook: Workbook, path_directory: str, filename: str) -> None:
        """
        Save a workbook to the specified directory path.
        :param filename: file name of the new excell.
        :param workbook: The workbook to save.
        :param path_directory: The directory path to save the workbook.
        """
        filepath = os.path.join(path_directory, filename)
        filepath_with_extension = filepath + ".xlsx"
        workbook.save(filepath_with_extension)
