from datetime import datetime

import pytest

from src.utils import get_start_end_month, round_to_limit

# def test_get_start_end_month() -> None:
#     start = datetime.strptime('2024-10-01', "%Y-%m-%d")
#     end = datetime.strptime('2024-10-31', "%Y-%m-%d")
#     assert get_start_end_month('2024-10-15') == (start, end)


def test_round_to_limit() -> None:
    assert round_to_limit(173, 50) == 27