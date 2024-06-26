import os
from datetime import datetime
from pprint import pprint

import pandas as pd
import requests

from dotenv import load_dotenv

from src.utils import get_data_from_excel

load_dotenv()
PATH_TO_DATA = os.getenv("PATH_TO_DATA")


def get_greeting(date: str) -> str:
    """ Принимает строку с датой и временем в формате (2024-01-01 00:00:00),
    возвращает приветствие: «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»"""
    hour = int(date.split()[1].split(':')[0])
    greeting = ''
    if hour in range(0, 6):
        greeting = 'Доброй ночи'
    elif hour in range(6, 12):
        greeting = 'Доброе утро'
    elif hour in range(12, 18):
        greeting = 'Добрый день'
    elif hour in range(18, 24):
        greeting = 'Добрый вечер'
    return greeting


def get_all_expenses(df: pd.DataFrame) -> list[dict]:
    """ Принимает DataFrame с банковскими операциями, возвращает список словарей,
    подсчитывает все расходы по карте и кешбэк"""
    if df.empty:
        return []
    expenses = df.loc[df['Сумма платежа'] < 0].groupby('Номер карты').agg({'Сумма операции': 'sum'})
    result = []
    dict_data = expenses.to_dict().get('Сумма операции')
    for key, item in dict_data.items():
        result.append({'last_digits': key[-4:],
                       'total_spent': item * -1,
                       'cashback': round(item / -100, 2)
                       })
    return result


def get_beginning_month(date: str) -> str:
    """ Принимает дату и возвращает начало месяца от переданной даты"""
    try:
        beginning = datetime.strptime(date, '%d.%m.%Y %H:%M:%S').replace(day=1, hour=0, minute=0, second=0,
                                                                         microsecond=0)
    except Exception as ex:
        print(ex)
        return ''
    return beginning.strftime('%d.%m.%Y %H:%M:%S')


def get_top_n_transactions(df: pd.DataFrame, date=None, n: int = 5) -> list[dict]:
    """ Принимает DataFrame с банковскими операциями и дату, возвращает список словарей,
    top 5 транзакций по сумме платежа, с начала месяца по переданную дату."""
    if date is None:
        date = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        beginning = get_beginning_month(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        beginning = pd.to_datetime(beginning, dayfirst=True)
        date = pd.to_datetime(date, dayfirst=True)
    else:
        try:
            beginning = pd.to_datetime(get_beginning_month(date), dayfirst=True)
            date = pd.to_datetime(date, dayfirst=True)
        except Exception as ex:
            print(ex)
            return []
    if df.empty:
        return []
    df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], dayfirst=True)
    filtered_df = df[(df['Дата платежа'].between(beginning, date))]

    filtered_df['Дата платежа'] = filtered_df['Дата платежа'].dt.strftime('%d.%m.%Y')
    top_n = filtered_df.sort_values(by='Сумма платежа', ascending=False).head(n).to_dict(orient='records')

    result = []
    for item in top_n:
        result.append({
            'date': item.get('Дата платежа'),
            'amount': item.get('Сумма платежа'),
            'category': item.get('Категория'),
            'description': item.get('Описание'),

        })
    return result


def currency_exchange_rate(currency: str) -> float:
    """Принимает название валюты и возвращает ее курс к рублю"""
    params = {"apikey": os.getenv("API_KEY_FOR_APILAYER")}
    response = requests.get(
        f"https://api.apilayer.com/fixer/latest?base={currency.upper()}&symbols=RUB", params=params
    )
    pprint(response.json(), indent=4)
    return float(response.json()["rates"]["RUB"])


def get_stock_price(stock: str) -> float:
    """Принимает название акции и возвращает ее цену"""
    params = {"apikey": os.getenv("API_KEY_FOR_ALPHAVANTAGE")}
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock.upper()}&apikey={params}"
    try:
        response = requests.get(url)
        result = response.json().get('Global Quote', None).get('05. price', None)
        result = round(float(result), 2)
    except Exception as ex:
        print(ex)
        result = None
    return result


def get_exchange_rates(currencies=None) -> list[dict]:
    """ Принимает список валют, возвращает список словарей с курсами валют"""

    if currencies is None:
        currencies = ['USD', 'EUR']
    result = []
    for currency in currencies:
        result.append({
            'currency': currency,
            'rate': round(currency_exchange_rate(currency), 2)
        })
    return result


def get_stocks_prices(stocks=None) -> list[dict]:
    """ Принимает список акций, возвращает список словарей с ценами акций"""

    if stocks is None:
        stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    result = []
    for stock in stocks:
        result.append({
            'stock': stock,
            'price': get_stock_price(stock)
        })
    return result


if __name__ == '__main__':

    # print(get_stock_price('GOOGL'))
    # df = get_data_from_excel(os.path.join(PATH_TO_DATA, 'test.xlsx'))
    df = get_data_from_excel(os.path.join(PATH_TO_DATA, 'operations.xlsx'))
    # list_dict = get_stocks_prices()
    # pprint(list_dict, indent=4)
    # pprint(list_dict, indent=4, sort_dicts=False)
    pprint(get_top_n_transactions(df, '31.12.2021 16:44:00'), indent=4)
