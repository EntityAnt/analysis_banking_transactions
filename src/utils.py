import os.path
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
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
            logger.info(f"Прочитаны данные из файла {path}")
            return result
        except Exception as ex:
            logger.error(f"Ошибка:  {ex}")
            return pd.DataFrame()
    else:
        logger.error("Файл не найден!")
        return pd.DataFrame()


def get_date_n_months_later(str_date: str, n: int = 3) -> datetime:
    """Принимает строку с датой в формате DD.MM.YYYY, возвращает дату n-месяцами ранее
    Функция отнимает n месяцев, но не n*30 дней. От 31 и 30 мая, при n=3 получаем 28 февраля
    (если год не високосный)"""
    try:
        date = datetime.strptime(str_date, "%d.%m.%Y")
        new_date = date + relativedelta(months=-n)
    except Exception as ex:
        logger.error(f"Некорректная дата {str_date} {ex}")
        return None

    return new_date


def str_title(string: str) -> str:
    """Принимает строку и возвращает строку, где только первая буква
    первого слова заглавная, остальные - прописные"""
    if string == '':
        return ''
    result = string.split()
    if len(result) == 1:
        return result[0].title()
    first_word = result[0].title()
    others_words = " ".join(result[1:])
    result = first_word + " " + others_words.lower()

    return result
