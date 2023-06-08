import unittest

from nice_functions import NiceExcelFunction


class TestNiceExcelFunction(unittest.TestCase):
    def test_get_column_index_from_letter(self):
        self.assertEqual(NiceExcelFunction.get_column_index_from_letter('A'), 1)
        self.assertEqual(NiceExcelFunction.get_column_index_from_letter('Z'), 26)
        self.assertEqual(NiceExcelFunction.get_column_index_from_letter('AA'), 27)
        self.assertEqual(NiceExcelFunction.get_column_index_from_letter('AB'), 28)
        self.assertEqual(NiceExcelFunction.get_column_index_from_letter('BA'), 53)
        self.assertEqual(NiceExcelFunction.get_column_index_from_letter('ZZ'), 702)

    def test_get_column_letter_from_index(self):
        self.assertEqual(NiceExcelFunction.get_column_letter_from_index(1), 'A')
        self.assertEqual(NiceExcelFunction.get_column_letter_from_index(26), 'Z')
        self.assertEqual(NiceExcelFunction.get_column_letter_from_index(27), 'AA')
        self.assertEqual(NiceExcelFunction.get_column_letter_from_index(28), 'AB')
        self.assertEqual(NiceExcelFunction.get_column_letter_from_index(53), 'BA')
        self.assertEqual(NiceExcelFunction.get_column_letter_from_index(702), 'ZZ')