import os
from datetime import datetime
from typing import Any

import pandas as pd
from dotenv import load_dotenv

from src.logger import setup_logging
from src.utils import get_date_n_months_later, get_data_from_excel

load_dotenv()
PATH_TO_DATA = os.getenv("PATH_TO_DATA")

logger = setup_logging(f'reports.py - {datetime.today().strftime("%Y-%m-%d")}')


def write_to_file_without_name(func) -> Any:
    def inner(*args, **kwargs) -> Any:
        name = f"{datetime.today().strftime('%d_%m_%Y')} - {func.__name__}.json"
        path = os.path.join(PATH_TO_DATA, name)
        result = func(*args, **kwargs)
        with open(path, "w", encoding="utf-8") as file:
            file.write(result.to_json(force_ascii=False, indent=4, orient="records"))
            logger.info(f"Результат работы функции {func.__name__} записан в файл {name}")

    return inner


def write_to_file_with_name(arg) -> Any:
    def decorator(func) -> Any:
        name = f"{arg}.xlsx"
        path = os.path.join(PATH_TO_DATA, name)

        def wrapper(*args, **kwargs) -> None:
            result = func(*args, **kwargs)
            result.to_excel(path, index=False)
            logger.info(f"Результат работы функции {func.__name__} записан в файл {name}")
            # with open(path, 'w', encoding='utf-8') as file:
            #     file.write(result.to_json(force_ascii=False, indent=4, orient='records'))

        return wrapper

    return decorator


# @write_to_file_without_name
# @write_to_file_with_name('Траты по категории')
def spending_by_category(df: pd.DataFrame, category: str, date: str = None) -> pd.DataFrame:
    """Функция принимает на вход:
        датафрейм с транзакциями,
        название категории,
        опциональную дату.
    Если дата не передана, то берется текущая дата.
    Возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    if df.empty:
        logger.warning("Траты по категориям - DataFrame пуст!")
        return pd.DataFrame()

    if date is None:
        end_date = datetime.now().strftime("%d.%m.%Y")
        logger.warning("Траты по категориям - Выбрана текущая дата!")
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y")
    start_date = get_date_n_months_later(date, 3)
    logger.info(f"Траты по категориям - Выбран период с {start_date} по {end_date}")

    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    filtered_df_by_data = df[(df["Дата платежа"].between(start_date, end_date, inclusive="both"))]
    pd.options.mode.chained_assignment = None
    filtered_df_by_data["Дата платежа"] = filtered_df_by_data["Дата платежа"].dt.strftime("%d.%m.%Y")
    filtered_df_by_category = filtered_df_by_data.loc[
        (filtered_df_by_data["Категория"] == category) & (filtered_df_by_data["Сумма платежа"] < 0)
    ]
    logger.info(f"Сформированы данные по категории {category} за период с {start_date} по {end_date}")
    return filtered_df_by_category


df = get_data_from_excel(os.path.join(PATH_TO_DATA, "test2.xlsx"))
print(type(spending_by_category(df, 'Супермаркеты', '30.12.2021')))