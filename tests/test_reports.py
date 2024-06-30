import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category():
    assert spending_by_category(pd.DataFrame).empty
