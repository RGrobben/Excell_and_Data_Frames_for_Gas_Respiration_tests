import pandas as pd


def find_outliers_of_specific_column(data_frame: pd.DataFrame, column_name: str) -> {}:
    """
    Find outliers in a DataFrame's column using the IQR method.

    Parameters:
    df : pd.DataFrame
        Input DataFrame.
    column : str
        Column name in the DataFrame to find outliers in.

    Returns:
    List[Tuple[int, str]]:
        List of tuples containing index and column name of outliers.
    """
    # loose Column
    loose_column = data_frame[column_name]

    # Calculate the IQR of the column
    Q1 = loose_column.quantile(0.25)
    Q3 = loose_column.quantile(0.75)
    IQR = Q3 - Q1
    under_boundary = Q1 - 1.5 * IQR
    outer_boundary = Q3 + 1.5 * IQR

    # Define outlier indexes
    indexes = []
    outliers = []
    for index in data_frame.index:
        value = loose_column[index]
        if value < under_boundary or value > outer_boundary:
            indexes.append(index)
            outliers.append(value)

    if len(indexes) > 0:
        return {column_name: {"indexes": indexes}, {"outliers": outliers}}
