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
            logger.info(f'Прочитаны данные из файла {path}')
            return result
        except Exception as ex:
            logger.error(f"Ошибка:  {ex}")
            return pd.DataFrame()
    else:
        logger.error(f"Файл не найден!")
        return pd.DataFrame()


def get_date_n_months_later(str_date: str, n: int = 3) -> datetime:
    """ Принимает строку с датой в формате DD.MM.YYYY, возвращает дату n-месяцами ранее"""
    try:
        date = datetime.strptime(str_date, '%d.%m.%Y')
        new_date = date + relativedelta(months=-n)
    except Exception as ex:
        print(ex)
        return None

    return new_date


# get_data_from_excel(os.path.join(PATH_TO_DATA, 'o.xlsx'))
