from datetime import datetime

from src.utils import get_date_n_months_later


def test_get_date_n_months_later() -> None:
    assert get_date_n_months_later('31.05.2024', 3) == datetime(2024, 2, 29, 00, 00, 00)
