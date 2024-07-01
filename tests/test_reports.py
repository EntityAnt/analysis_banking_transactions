import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(get_empty_df: pd.DataFrame, get_full_df: pd.DataFrame) -> None:
    assert spending_by_category(get_empty_df, "Супермаркеты", "28.08.2021").empty
    assert spending_by_category(get_empty_df, "Супермаркеты", "28.08.2021").any
    assert type(spending_by_category(get_empty_df, "Супермаркеты", "28.08.2021")) == pd.core.frame.DataFrame
