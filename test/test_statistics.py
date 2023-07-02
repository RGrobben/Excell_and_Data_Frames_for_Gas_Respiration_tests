# Test class
import unittest

import numpy as np
import pandas as pd

from statistics.statistics import find_column_outliers


class TestFindColumnOutliers(unittest.TestCase):

    def test_find_column_outliers_random(self):
        np.random.seed(0)  # for reproducibility
        df = pd.DataFrame({'A': np.random.normal(0, 1, 100), 'B': np.random.normal(0, 1, 100)})

        # Introduce outliers
        df.at[0, 'A'] = 10  # Upper outlier
        df.at[1, 'A'] = -10  # Lower outlier

        result = find_column_outliers(df, 'A')

        expected_indexes = [0, 1]
        expected_values = [10.0, -10.0]

        self.assertEqual(result['A']['indexes'], expected_indexes)
        self.assertEqual(result['A']['outliers'], expected_values)

    def test_find_column_outliers(self):
        df_1 = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                  21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                  41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 1000, -1000]})  # Last two values are outliers
        result_A = find_column_outliers(df_1, 'A')
        expected_indexes_A = [50, 51]
        expected_values_A = [1000, -1000]

        self.assertEqual(result_A['A']['indexes'], expected_indexes_A)
        self.assertEqual(result_A['A']['outliers'], expected_values_A)

    def test_find_column_outliers_no_outliers(self):
        df_2 = pd.DataFrame({
            'B': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                  21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                  41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52]})
        result_B = find_column_outliers(df_2, 'B')
        expected_indexes_B = []
        expected_values_B = []

        self.assertEqual(result_B['B']['indexes'], expected_indexes_B)
        self.assertEqual(result_B['B']['outliers'], expected_values_B)

    def test_find_column_outliers_in_middle(self):
        df_1 = pd.DataFrame({
            'A': list(range(1, 51)) + [1000, -1000] + list(range(51, 101))})  # Outliers in the middle
        result_A = find_column_outliers(df_1, 'A')
        expected_indexes_A = [50, 51]
        expected_values_A = [1000, -1000]

        self.assertEqual(result_A['A']['indexes'], expected_indexes_A)
        self.assertEqual(result_A['A']['outliers'], expected_values_A)

    def test_find_column_outliers_random_in_great_data_set(self):
        df_2 = pd.DataFrame({
            'B': list(range(1, 26)) + [1000] + list(range(26, 76)) + [-1000] + list(range(76, 101))})  # Random outliers
        result_B = find_column_outliers(df_2, 'B')
        expected_indexes_B = [25, 76]
        expected_values_B = [1000, -1000]

        self.assertEqual(result_B['B']['indexes'], expected_indexes_B)
        self.assertEqual(result_B['B']['outliers'], expected_values_B)


if __name__ == '__main__':
    unittest.main()




