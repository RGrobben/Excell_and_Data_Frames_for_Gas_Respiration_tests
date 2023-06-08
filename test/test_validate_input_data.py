import unittest

import numpy as np
import pandas as pd

from validate_input_data import ValidateInputData, validate_if_there_is_a_float_or_integer_in_cell


class DataFrameValidationTest(unittest.TestCase):
    def test_valid_data_frame(self):
        # Create a valid DataFrame with float and integer values
        data = {'ColumnA': [1, 2.5, 3, 4.7, 5], 'ColumnB': [1.2, 2, 3.8, 4, 5]}
        df = pd.DataFrame(data)

        # Call the function and expect an empty list as the result
        result = validate_if_there_is_a_float_or_integer_in_cell(df, 'ColumnA')
        self.assertEqual(result, True)

    def test_invalid_data_frame(self):
        # Create an invalid DataFrame with non-numeric values
        data = {'ColumnA': [1, '2.5', 3, 'abc', 5], 'ColumnB': [1.2, 2, 3.8, 4, 5]}
        df = pd.DataFrame(data)

        # Call the function and expect a list of invalid row indices
        result = validate_if_there_is_a_float_or_integer_in_cell(df, 'ColumnA')
        self.assertEqual(result, [1, 3])


# class TestValidateInputData_:
#     def test_validate_if_there_are_dates(self):
#         column_name_date = "Date"
#
#         data = {column_name_date: ["2023/04/17", "2023/04/19", "2023/04/24", "2023/04/24", "2023/04/26", "2023/04/26",
#                                    "2023/04/28", "2023/05/01", "2023/05/01", "2023/05/04", "2023/05/04", "2023/05/08",
#                                    "2023/05/08", "2023/05/10", "2023/05/10", "2023/05/12", "2023/05/12", "2023/05/15",
#                                    "2023/05/15", "2023/05/17", "2023/05/17", "2023/05/22", "2023/05/22"]
#                 }
#
#         data_frame = pd.DataFrame(data)
#         pass
class TestValidateInputData(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.date_column = "DateColumn"
        self.df = pd.DataFrame({
            self.date_column: ['2022-01-01', '2022-02-01', '2022-03-01']
        })

    def test_validate_if_there_are_dates_column_does_not_exist(self):
        validator = ValidateInputData(self.df)
        result = validator.validate_if_there_are_dates('NonExistentColumn')
        expected = "Column 'NonExistentColumn' does not exist in the data frame."
        self.assertEqual(result, expected)

    def test_validate_if_there_are_dates_correct_dates(self):
        validator = ValidateInputData(self.df)
        try:
            validator.validate_if_there_are_dates(self.date_column)
        except AssertionError:
            pass

    def test_validate_if_there_are_dates_wrong_dates(self):
        data_frame = self.df
        data_frame[self.date_column].at[1] = "2023-5-3"  # Modify a date to be incorrect
        validator = ValidateInputData(data_frame)
        result = validator.validate_if_there_are_dates(self.date_column)
        expected = "The following rows have wrong dates [1]"
        self.assertEqual(expected, result)
