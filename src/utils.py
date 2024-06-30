import os.path
from datetime import datetime, timedelta

import pandas as pd
from dotenv import load_dotenv

from src.logger import setup_logging

load_dotenv()
PATH_TO_DATA = os.getenv("PATH_TO_DATA")

logger = setup_logging(f'utils.py - {datetime.today().strftime("%Y-%m-%d")}')


def get_data_from_excel(path: str) -> pd.DataFrame:
    """Читает данные и excel-файла и возвращает DataFrame."""
    if os.path.isfile(path):
        try:
            result = pd.read_excel(path)
            logger.info(f'\nПрочитаны данные из файла {path}')
            return result
        except Exception as ex:
            logger.error(f"Ошибка:  {ex}")
            return pd.DataFrame()
    else:
        logger.error(f"Файл не найден!")
        return pd.DataFrame()


def get_start_end_month(date: str) -> tuple():
    """Принимает строку с датой в формате 'YYYY-MM-DD', возвращает кортеж с датами начала и конца месяца"""

    start = datetime.strptime(date, "%Y-%m-%d")
    year = start.year
    month = start.month
    if month != 12:
        end = datetime.strptime(f"{year}-{month + 1}-01", "%Y-%m-%d") - timedelta(days=1)
    else:
        end = datetime.strptime(f"{year + 1}-01-01", "%Y-%m-%d") - timedelta(days=1)

    return start, end


def transactions_from_df(df: pd.DataFrame) -> list[dict]:
    """Принимает DataFrame, возвращает список словарей с датой операции и суммой"""

    data = df.to_dict(orient="records")
    result = []
    for item in data:
        result.append(
            {
                "Дата операции": datetime.strptime(item.get("Дата операции"), "%d.%m.%Y %H:%M:%S").strftime(
                    "%Y-%m-%d"
                ),
                "Сумма операции": item.get("Сумма операции"),
            }
        )
    logger.info('Сформированы данные с датой операции и суммой')
    return result


def round_to_limit(amount: float, limit: int) -> float:
    """Принимает сумму и лимит, до которого надо округлить,
    возвращает разницу между исходной и округленной суммами"""
    result = amount + (limit - amount % limit)
    logger.info(f'round_to_limit - сумма {amount}, лимит - {limit}, округлили до {result}')
    return round(result - amount, 2)


