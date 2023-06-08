from datetime import datetime

import pandas as pd


def validate_if_there_is_a_float_or_integer_in_cell(data_frame: pd.DataFrame, column_name: str) -> []:
    invalid_rows = []
    column_in_data_frame_to_be_checked = data_frame[column_name]
    for index in column_in_data_frame_to_be_checked.index:
        value = column_in_data_frame_to_be_checked[index]
        if not isinstance(value, (float, int)):
            invalid_rows.append(index)

    if len(invalid_rows) > 0:
        return invalid_rows
    else:
        return True


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

    def validate_if_there_are_P_atmosphere(self):
        pass

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
