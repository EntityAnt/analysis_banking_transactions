import json
import os
import locale

from calendar import month_name
from datetime import datetime
from pprint import pprint

from src.logger import setup_logging
from src.services import analysis_categories_cashback, investment_bank
from src.utils import get_data_from_excel, transactions_from_df
from dotenv import load_dotenv

load_dotenv()
PATH_TO_DATA = os.getenv('PATH_TO_DATA')

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

logger = setup_logging(f'services.py - {datetime.today().strftime("%Y-%m-%d")}')


def main_services() -> None:
    """Функция реализует весь функционал модуля services.py"""
    df = get_data_from_excel(os.path.join(os.getenv("PATH_TO_DATA"), "operations.xlsx"))
    print('Для анализа кешбэка по категориям')
    while True:
        try:
            year = int(input('Ведите год: ').strip())
        except Exception as ex:
            logger.error(f'\nОшибка: {ex}')
            continue
        if (year > 2021) or (year < 2018):
            print('Для анализа доступны данные с 2018 по 2021 года включительно!')
            continue
        while True:
            try:
                month = int(input('Ведите месяц: ').strip())
            except Exception as ex:
                logger.error(f'Ошибка: {ex}')
                continue
            if (month < 1) or (month > 12):
                print('Такого месяца не существует!')
                continue
            break
        break

    print('*' * 50)
    print(f'Выбран {year} год, месяц - {month_name[month]} ')
    res_dict = json.loads(analysis_categories_cashback(df, year, month))
    for key, item in res_dict.items():
        print(f'Категория: "{key}" - заработано кешбэка {item} руб.')

    print('-' * 50)
    while True:
        try:
            limit = int(input('Введите лимит округления (10, 50, 100): ').strip())
        except Exception as ex:
            logger.error(f'Ошибка: {ex}')
            continue
        if limit not in [10, 50, 100]:
            continue
        break

    transactions = transactions_from_df(df)
    year_month = f'{year}-{month}'
    piggy = round(investment_bank(year_month, transactions, limit), 2)

    print('*' * 50)
    print(
        f' В {year} году, месяц-{month_name[month]}, при лимите округления {limit}, можно было отложить {piggy} руб.')


if __name__ == '__main__':
    main_services()
