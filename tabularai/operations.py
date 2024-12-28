"""Allowed pandas operations."""

import pandas as pd


def transpose(df: pd.DataFrame) -> pd.DataFrame:
    """Transpose dataframe."""
    return df.transpose() # type: ignore

def slice(df: pd.DataFrame, x: int, y: int) -> pd.DataFrame:
    """Transpose dataframe."""
    return df.iloc[x:,y:]




