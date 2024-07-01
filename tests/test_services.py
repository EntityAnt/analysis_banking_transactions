import json

import pandas as pd
import pytest

from src.services import analysis_categories_cashback, investment_bank


def test_analysis_categories_cashback(get_empty_df: pd.DataFrame, get_full_df: pd.DataFrame) -> None:
    assert analysis_categories_cashback(get_empty_df, 2021, 11) == {}
    result = analysis_categories_cashback(get_full_df, 2021, 11)
    expected = json.dumps({"Супермаркеты": 570.0, "Аптеки": 175.0, "Дом и ремонт": 52.0}, ensure_ascii=False)
    assert result == expected


@pytest.mark.parametrize(
    "month, limit, expected",
    [
        ("2021-11", 10, 1186.79),
        ("2021-11", 50, 4996.79),
        ("2021-11", 100, 10096.789999999997),
        ("2024-11", 10, 0),
    ],
)
def test_investment_bank(month, get_full_transactions: list[dict], limit, expected) -> None:
    assert investment_bank(month, get_full_transactions, limit) == expected
