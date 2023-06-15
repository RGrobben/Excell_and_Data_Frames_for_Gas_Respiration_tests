import pandas as pd
from typing import Dict, List, Union


def find_column_outliers(data_frame: pd.DataFrame, column_name: str, return_only_indexes: bool = False)\
        -> Dict[str, Dict[str, List[Union[int, float]]]]:
    """
    Finds outliers in a specified column of a DataFrame using the IQR method.

    Parameters:
    data_frame : pd.DataFrame
        Input DataFrame.
    column_name : str
        Column name in the DataFrame to find outliers in.

    Returns:
    dict: A dictionary with the column name as the key. The value is another dictionary with two keys: 'indexes'
        and 'outliers'. 'indexes' holds a list of the indices of the outliers in the original DataFrame. 'outliers'
        contains a list of the outlier values.
    """
    # Calculate the IQR of the column
    Q1 = data_frame[column_name].quantile(0.25)
    Q3 = data_frame[column_name].quantile(0.75)
    IQR = Q3 - Q1

    # Define the outlier boundaries
    under_boundary = Q1 - 1.5 * IQR
    outer_boundary = Q3 + 1.5 * IQR

    # Identify the outliers
    outliers_mask = ((data_frame[column_name] < under_boundary) | (data_frame[column_name] > outer_boundary))
    outlier_indexes = data_frame[outliers_mask].index.tolist()
    outlier_values = data_frame[column_name][outliers_mask].tolist()

    if return_only_indexes:
        return outlier_indexes

    return {column_name: {"indexes": outlier_indexes, "outliers": outlier_values}}
