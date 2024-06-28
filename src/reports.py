import csv
import json
import os
from datetime import datetime
from pprint import pprint

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import get_data_from_excel
from dotenv import load_dotenv

load_dotenv()
PATH_TO_DATA = os.getenv("PATH_TO_DATA")


def write_to_file_without_name(func):
    name = f"{datetime.today().strftime('%d_%m_%Y')} - {func.__name__}.json"
    path = os.path.join(PATH_TO_DATA, name)

    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(result.to_json(force_ascii=False, indent=4, orient='records'))

    return inner


def write_to_file_with_name(arg):
    def decorator(func):
        name = f"{arg}.xlsx"
        path = os.path.join(PATH_TO_DATA, name)

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result.to_excel(path, index=False)
            # with open(path, 'w', encoding='utf-8') as file:
            #     file.write(result.to_json(force_ascii=False, indent=4, orient='records'))

        return wrapper

    return decorator


# @write_to_file_without_name
# @write_to_file_with_name('Траты по категории')
def spending_by_category(df: pd.DataFrame, category: str, date: str = None) -> pd.DataFrame:
    """ Функция принимает на вход:
            датафрейм с транзакциями,
            название категории,
            опциональную дату.
        Если дата не передана, то берется текущая дата.
        Возвращает траты по заданной категории за последние три месяца (от переданной даты). """
    if df.empty:
        return pd.DataFrame()

    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, '%d.%m.%Y')

    start_date = get_date_n_months_later(date, 3)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    filtered_df_by_data = df[(df["Дата платежа"].between(start_date, end_date, inclusive="both"))]
    filtered_df_by_data["Дата платежа"] = filtered_df_by_data["Дата платежа"].dt.strftime("%d.%m.%Y")
    filtered_df_by_category = filtered_df_by_data.loc[(filtered_df_by_data['Категория'] == category) &
                                                      (filtered_df_by_data['Сумма платежа'] < 0)]

    return filtered_df_by_category


def get_date_n_months_later(str_date: str, n: int = 3) -> datetime:
    """ Принимает строку с датой в формате DD.MM.YYYY, возвращает дату n-месяцами ранее"""
    try:
        date = datetime.strptime(str_date, '%d.%m.%Y')
        new_date = date + relativedelta(months=-n)
    except Exception as ex:
        print(ex)
        return None

    return new_date


if __name__ == "__main__":
    # print(get_date_n_months_later('15.03.2018'))
    df = get_data_from_excel(os.path.join(os.getenv("PATH_TO_DATA"), "operations.xlsx"))
    spending_by_category(df, 'Супермаркеты', '17.12.2021')
