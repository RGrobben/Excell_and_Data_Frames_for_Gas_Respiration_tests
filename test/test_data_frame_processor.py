import unittest

import pandas as pd

from data_frame_processor import DataFrameProcessor


class TestDataFrameProcessor(unittest.TestCase):

    def test_add_day_column(self):
        date_column_name = "Date"
        time_column_name = "Time"
        day_column_name = "Day"

        data = {date_column_name:
                    ["17/04/2023", "19/04/2023", "24/04/2023", "24/04/2023", "26/04/2023", "26/04/2023", "28/04/2023",
                     "01/05/2023", "01/05/2023", "04/05/2023", "04/05/2023", "08/05/2023", "08/05/2023", "10/05/2023",
                     "10/05/2023", "12/05/2023", "12/05/2023", "15/05/2023", "15/05/2023", "17/05/2023", "17/05/2023",
                     "22/05/2023", "22/05/2023"],
                time_column_name: [ "14:42", "14:42", "10:20", "11:25", "08:52", "09:53", "09:45", "13:50", "14:49",
                                    "09:26", "10:46", "08:40", "09:47", "09:35", "10:40", "09:09", "10:10", "09:30",
                                    "10:38", "08:52", "09:57", "14:11", "15:08",]
        }

        df = pd.DataFrame(data)

        DataFrameProcessor.add_day_column(
            data_frame=df,
            date_column_name=date_column_name,
            time_column_name=time_column_name,
            day_column_name=day_column_name
        )

        expected_vales_day = [0.00000000000000000, 2.00000000000000000, 6.81805555555184000, 6.86319444444234000,
                              8.75694444443798000, 8.79930555555620000, 10.79374999999710000, 13.96388888888760000,
                              14.00486111110510000, 16.78055555555330000, 16.83611111110800000, 20.74861111110660000,
                              20.79513888888320000, 22.78680555555180000, 22.83194444444230000, 24.76874999999560000,
                              24.81111111110660000, 27.78333333333280000, 27.83055555555620000, 29.75694444443800000,
                              29.80208333332850000, 34.97847222221750000, 35.01805555555620000]
        for i in range(len(expected_vales_day)):
            self.assertAlmostEqual(expected_vales_day[i], df[day_column_name][i])
