import os.path
from io import StringIO
from unittest.mock import patch

import pytest
import pandas as pd

from src.utils import get_data_from_excel, currency_exchange_rate, get_stock_price, get_beginning_month
from dotenv import load_dotenv

load_dotenv()
PATH_TO_TESTS = os.getenv('PATH_TO_TESTS')
KEY_APILAYER = {"apikey": os.getenv("API_KEY_FOR_APILAYER")}
KEY_ALPHAVANTAGE = {"apikey": os.getenv("API_KEY_FOR_ALPHAVANTAGE")}


def test_get_data_from_excel():
    assert get_data_from_excel('').empty
    assert get_data_from_excel(os.path.join(PATH_TO_TESTS, 'test.xlsx')).any


@patch("requests.get")
def test_currency_exchange_rate(mock_get):
    mock_get.return_value.json.return_value = {
        "success": True,
        "timestamp": 1717678144,
        "base": "USD",
        "date": "2024-06-06",
        "rates": {"RUB": 88.848824},
    }
    assert currency_exchange_rate("USD") == 88.848824
    mock_get.assert_called_once_with("https://api.apilayer.com/fixer/latest?base=USD&symbols=RUB", params=KEY_APILAYER)


@patch("requests.get")
def test_get_stock_price(mock_get):
    mock_get.return_value.json.return_value = {'Global Quote':
        {
            '01. symbol': 'AAPL',
            '02. open': '215.7700',
            '03. high': '216.0700',
            '04. low': '210.3000',
            '05. price': '210.6200',
            '06. volume': '82542718',
            '07. latest trading day': '2024-06-28',
            '08. previous close': '214.1000',
            '09. change': '-3.4800',
            '10. change percent': '-1.6254%'
        }
    }
    assert get_stock_price("AAPL") == 210.62
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={KEY_ALPHAVANTAGE}"
    mock_get.assert_called_once_with(url)


def test_get_beginning_month():
    assert get_beginning_month('') == ''
    assert get_beginning_month('31.12.2021 15:44:39') == '01.12.2021 00:00:00'