import os.path
from typing import Callable

import pandas as pd
import pytest

from src.views import get_greeting, get_all_expenses, get_top_n_transactions
from dotenv import load_dotenv

load_dotenv()

PATH_TO_TESTS = os.getenv('PATH_TO_TESTS')
PATH_TO_DATA = os.getenv('PATH_TO_DATA')


@pytest.mark.parametrize('date, expected', [
    ('2024-01-01 03:00:00', 'Доброй ночи'),
    ('2024-01-01 08:00:00', 'Доброе утро'),
    ('2024-01-01 14:00:00', 'Добрый день'),
    ('2024-01-01 20:00:00', 'Добрый вечер'),
]
                         )
def test_get_greeting(date: str, expected: str) -> None:
    assert get_greeting(date) == expected


def test_get_all_expenses(get_test1_df: Callable, get_empty_df: Callable) -> None:
    result = get_all_expenses(get_test1_df)
    assert result == [{'last_digits': '7197', 'total_spent': 210, 'cashback': 2.1}]
    result = get_all_expenses(get_empty_df)
    assert result == []


def test_get_top_n_transactions(get_full_df: Callable, get_empty_df: Callable, result_for_top_n) -> None:
    result = get_top_n_transactions(get_full_df, is_debit=True, date='30.06.2021 16:44:00')
    assert result == result_for_top_n
    result = get_all_expenses(get_empty_df)
    assert result == []
