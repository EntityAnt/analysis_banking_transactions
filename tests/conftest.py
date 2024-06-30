import os

import pandas as pd
import pytest
from dotenv import load_dotenv

load_dotenv()

PATH_TO_TESTS = os.getenv("PATH_TO_TESTS")
PATH_TO_DATA = os.getenv("PATH_TO_DATA")


@pytest.fixture()
def get_test1_df() -> pd.DataFrame:
    return pd.read_excel(os.path.join(PATH_TO_TESTS, "test1.xlsx"))


@pytest.fixture()
def get_empty_df() -> pd.DataFrame:
    return pd.DataFrame()


@pytest.fixture()
def get_full_df() -> pd.DataFrame:
    path = os.path.join(PATH_TO_DATA, "operations.xlsx")
    return pd.read_excel(path)


