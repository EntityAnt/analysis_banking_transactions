from datetime import datetime

import pytest

from src.utils import get_date_n_months_later, str_title


@pytest.mark.parametrize('date, n, expected', [
    ('31.05.2024', 3, datetime(2024, 2, 29, 00, 00, 00)),
    ('30.05.2024', 3, datetime(2024, 2, 29, 00, 00, 00)),

]
                         )
def test_get_date_n_months_later(date: str, n: int, expected: datetime) -> None:
    assert get_date_n_months_later('31.05.2024', 3) == expected


@pytest.mark.parametrize(
    'string, expected',
    [
        ('', ''),
        ('Test', 'Test'),
        ('test', 'Test'),
        ('tEST', 'Test'),
        ('Test Test Test Test', 'Test test test test'),
        ('Test TEST tEST test', 'Test test test test'),
    ]
)
def test_str_title(string: str, expected: str) -> None:
    assert str_title(string) == expected