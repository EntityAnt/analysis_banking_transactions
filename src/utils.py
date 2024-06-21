import os.path

import pandas as pd

from dotenv import load_dotenv

load_dotenv()
PATH_TO_DATA = os.getenv("PATH_TO_DATA")


def get_data_from_excel(path: str) -> pd.DataFrame:
    """Читает данные и excel-файла и возвращает DataFrame."""

    result = pd.read_excel(path).to_json(orient="records", indent=4, force_ascii=False)
    return result


if __name__ == '__main__':
    print(get_data_from_excel(os.path.join(PATH_TO_DATA, 'operations.xlsx')))
