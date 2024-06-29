import pytest
from datetime import datetime

from src.utils import get_start_end_month


def test_get_start_end_month() -> None:
    start = datetime.strptime('2024-10-01', "%Y-%m-%d")
    end = datetime.strptime('2024-10-31', "%Y-%m-%d")
    assert get_start_end_month('2024-10-15') == (start, end)