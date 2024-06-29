import os.path
from datetime import datetime

import pandas as pd
import requests

from dotenv import load_dotenv

from src.logger import setup_logging

load_dotenv()
PATH_TO_DATA = os.getenv("PATH_TO_DATA")
PATH_TO_TESTS = os.getenv("PATH_TO_TESTS")

logger = setup_logging(f'utils.py - {datetime.today().strftime("%Y-%m-%d")}')


def get_data_from_excel(path: str) -> pd.DataFrame:
    """Читает данные и excel-файла и возвращает DataFrame."""
    if os.path.isfile(path):
        try:
            result = pd.read_excel(path)
            logger.info(f'Прочитаны данные из файла {path}')
            return result
        except Exception as ex:
            logger.error(f"Ошибка:  {ex}")
            return pd.DataFrame()
    else:
        logger.error(f"Файл не найден!")
        return pd.DataFrame()


def get_stock_price(stock: str) -> float:
    """Принимает название акции и возвращает ее цену"""
    params = {"apikey": os.getenv("API_KEY_FOR_ALPHAVANTAGE")}
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock.upper()}&apikey={params}"
    try:
        response = requests.get(url)
        print(response.json())
        result = response.json().get("Global Quote", None).get("05. price", None)
        result = round(float(result), 2)
        logger.info(f'Получены данные с https://api.apilayer.com')
    except Exception as ex:
        logger.error(f'Ошибка получения данных с API - {ex}')
        result = 0.0
    return result


def currency_exchange_rate(currency: str) -> float:
    """Принимает название валюты и возвращает ее курс к рублю"""
    params = {"apikey": os.getenv("API_KEY_FOR_APILAYER")}
    try:
        response = requests.get(
            f"https://api.apilayer.com/fixer/latest?base={currency.upper()}&symbols=RUB", params=params
        )
        result = float(response.json()["rates"]["RUB"])
        logger.info(f'Получены данные с https://api.apilayer.com')
    except Exception as ex:
        logger.error(f'Ошибка получения данных с API - {ex}')
    return result


def get_beginning_month(date: str) -> str:
    """Принимает дату и возвращает начало месяца от переданной даты"""
    try:
        beginning = datetime.strptime(date, "%d.%m.%Y %H:%M:%S").replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
    except Exception as ex:
        logger.error(ex)
        return ""
    return beginning.strftime("%d.%m.%Y %H:%M:%S")


# get_data_from_excel(os.path.join(PATH_TO_TESTS, 'test.xlsx'))
print(get_stock_price('AAPL'))