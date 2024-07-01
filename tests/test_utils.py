from datetime import datetime

import pandas as pd
import pytest

from src.utils import get_start_end_month, round_to_limit, transactions_from_df


def test_get_start_end_month() -> None:
    start = datetime.strptime("2024-10-01", "%Y-%m-%d")
    end = datetime.strptime("2024-10-31", "%Y-%m-%d")
    assert get_start_end_month("2024-10-15") == (start, end)


@pytest.mark.parametrize(
    "amount, limit, expected",
    [
        (173.50, 50, 26.5),
        (173.50, 10, 6.5),
        (173.50, 100, 26.5),
        (113.13, 10, 6.87),
        (113.13, 50, 36.87),
    ],
)
def test_round_to_limit(amount: float, limit: int, expected: float) -> None:
    assert round_to_limit(amount, limit) == expected


def test_transactions_from_df(get_test1_df: pd.DataFrame, get_empty_df: pd.DataFrame) -> None:
    assert transactions_from_df(get_empty_df) == []
    assert transactions_from_df(get_test1_df) == [
        {"Дата операции": "2018-01-17", "Сумма операции": -210},
        {"Дата операции": "2018-01-17", "Сумма операции": -4350},
    ]
