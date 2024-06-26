import os.path

import pytest
import pandas as pd

from src.utils import get_data_from_excel


def test_get_data_from_excel():
    path = os.path.join(os.getcwd(), 'test_excel.xlsx')
    assert get_data_from_excel(path) == pd.read_excel(path)
    # assert get_data_from_excel('') == []
