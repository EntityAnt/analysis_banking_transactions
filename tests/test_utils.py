import os.path
from io import StringIO

import pytest
import pandas as pd

from src.utils import get_data_from_excel
from dotenv import load_dotenv

load_dotenv()
PATH_TO_TESTS = os.getenv('PATH_TO_TESTS')


def test_get_data_from_excel(return_data_frame):
    assert get_data_from_excel('').empty
    assert get_data_from_excel(os.path.join(PATH_TO_TESTS, 'test.xlsx')).any
