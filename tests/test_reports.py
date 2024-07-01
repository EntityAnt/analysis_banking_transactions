import pandas
import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category(get_empty_df, get_full_df):
    assert spending_by_category(get_empty_df, 'Супермаркеты', '28.08.2021').empty
    assert spending_by_category(get_empty_df, 'Супермаркеты', '28.08.2021').any
    assert type(spending_by_category(get_empty_df, 'Супермаркеты', '28.08.2021')) == pandas.core.frame.DataFrame