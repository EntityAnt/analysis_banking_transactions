import os

import pandas as pd
import pytest

from dotenv import load_dotenv

load_dotenv()


@pytest.fixture()
def get_empty_df() -> pd.DataFrame:
    return pd.DataFrame()


@pytest.fixture()
def get_full_df() -> pd.DataFrame:
    path = os.path.join(os.getenv('PATH_TO_DATA'), "operations.xlsx")
    return pd.read_excel(path)
