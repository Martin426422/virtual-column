"""
Part 1 - Virtual Column
"""

import pandas as pd


def add_virtual_column(
    df: pd.DataFrame,
    expression: str,
    new_column_name: str
) -> pd.DataFrame:
    """
    Add a virtual column based on an arithmetic expression.
    Returns an empty DataFrame when the expression is invalid.
    """

    if not new_column_name:
        return pd.DataFrame()

    result = df.copy()

    try:
        result[new_column_name] = result.eval(expression)

    except Exception:
        return pd.DataFrame()

    return result
