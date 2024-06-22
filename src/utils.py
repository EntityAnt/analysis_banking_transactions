import os.path

import pandas as pd

from dotenv import load_dotenv

load_dotenv()
PATH_TO_DATA = os.getenv("PATH_TO_DATA")


def get_data_from_excel(path: str) -> pd.DataFrame:
    """Читает данные и excel-файла и возвращает DataFrame."""
    if os.path.isfile(path):
        try:
            result = pd.read_excel(path)
            return result
        except Exception as ex:
            print(ex)
            return []
    else:
        print("Файл не найден.")
        return []
