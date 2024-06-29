import os

import pytest
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

PATH_TO_TESTS = os.getenv('PATH_TO_TESTS')
PATH_TO_DATA = os.getenv('PATH_TO_DATA')


@pytest.fixture()
def get_test1_df():
    return pd.read_excel(os.path.join(PATH_TO_TESTS, 'test1.xlsx'))


@pytest.fixture()
def get_empty_df():
    return pd.DataFrame()


@pytest.fixture()
def get_full_df():
    return pd.read_excel(os.path.join(PATH_TO_DATA, 'operations.xlsx'))


@pytest.fixture()
def result_for_top_n():
    return [{'amount': 79159.51,
             'category': 'Переводы',
             'date': '22.06.2021',
             'description': 'Перевод Кредитная карта. ТП 10.2 RUR'},
            {'amount': 5000.0,
             'category': 'Бонусы',
             'date': '06.06.2021',
             'description': 'Компенсация покупки'},
            {'amount': 1100.0,
             'category': 'Пополнения',
             'date': '06.06.2021',
             'description': 'Внесение наличных через банкомат Тинькофф'},
            {'amount': 191.3,
             'category': 'Бонусы',
             'date': '16.06.2021',
             'description': 'Проценты на остаток'},
            {'amount': 186.0,
             'category': 'Бонусы',
             'date': '16.06.2021',
             'description': 'Вознаграждение за операции покупок'}]
