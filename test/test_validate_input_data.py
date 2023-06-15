import unittest

import pandas as pd

from Validation.general_validation_functions import validate_if_there_is_a_float_or_integer_in_cell, \
    validate_if_there_is_a_specific_string


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


class TestValidation(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        data = {'Column1': ['apple', 'banana', 'orange', 'grape'],
                'Column2': ['apple', 'banana', 'kiwi', 'melon']}
        self.df = pd.DataFrame(data)

        # Define the specific strings to validate against
        self.specific_strings = ['apple', 'banana']

    def test_validate_if_there_is_a_specific_string_1_return_true(self):
        # Test case 1: Valid values
        column_name, result = validate_if_there_is_a_specific_string(self.df, 'Column1', self.specific_strings)
        self.assertEqual(column_name, 'Column1')
        self.assertTrue(result)

    def test_validate_if_there_is_a_specific_string_2_return_indexes(self):
        # Test case 2: Invalid values
        column_name, result = validate_if_there_is_a_specific_string(self.df, 'Column2', self.specific_strings)
        self.assertEqual(column_name, 'Column2')
        self.assertEqual(result, [2, 3])

    def test_validate_if_there_is_a_specific_string_3_return_indexes(self):
        # Test case 3: Start row values table in Excel
        column_name, result = validate_if_there_is_a_specific_string(self.df, 'Column2', self.specific_strings,
                                                                     start_row_values_table_in_excel=2)
        self.assertEqual(column_name, 'Column2')
        self.assertEqual(result, [4, 5])

