import unittest

import numpy as np
import pandas as pd

from validate_input_data import ValidateInputData


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
        self.df['DateColumn'][1] = np.nan  # Modify a date to be incorrect
        validator = ValidateInputData(self.df)
        result = validator.validate_if_there_are_dates('DateColumn')
        expected = "The following rows have wrong dates [1]"
        self.assertEqual(expected, result)
