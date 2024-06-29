import pytest

from src.views import get_greeting


@pytest.mark.parametrize('date, expected', [
    ('2024-01-01 03:00:00', 'Доброй ночи'),
    ('2024-01-01 08:00:00', 'Доброе утро'),
    ('2024-01-01 14:00:00', 'Добрый день'),
    ('2024-01-01 20:00:00', 'Добрый вечер'),
]
                         )
def test_get_greeting(date: str, expected: str):
    assert get_greeting(date) == expected
