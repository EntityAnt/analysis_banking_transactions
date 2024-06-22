import os
from pprint import pprint

import pandas as pd

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


def get_top_transactions(df: pd.DataFrame, n: int = 5) -> list[dict]:
    """ Принимает DataFrame с банковскими операциями, возвращает список словарей,
    top 5 транзакций"""
    if df.empty:
        return []
    top_n = df.sort_values(by='Сумма платежа', ascending=False).head(n).to_dict(orient='records')
    result = []
    for item in top_n:
        result.append({
            'date': item.get('Дата платежа'),
            'amount': item.get('Сумма операции'),
            'category': item.get('Категория'),
            'description': item.get('Описание'),

        })
    return result


if __name__ == '__main__':

    # df = get_data_from_excel(os.path.join(PATH_TO_DATA, 'empty.xlsx'))
    df = get_data_from_excel(os.path.join(PATH_TO_DATA, 'operations.xlsx'))
    list_dict = get_top_transactions(df)
    pprint(list_dict, indent=4, sort_dicts=False)
