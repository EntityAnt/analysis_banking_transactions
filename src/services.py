import json
import os
from collections import defaultdict
from datetime import datetime, timedelta
from pprint import pprint

import pandas as pd

from src.utils import get_data_from_excel


def analysis_categories_cashback(data: pd.DataFrame, year: int, month: int) -> json:
    """ На вход функции поступают данные для анализа, год и месяц.
    На выходе — JSON с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года."""

    start_month = datetime.strptime(f'{year}-{month}-01', '%Y-%m-%d')
    if month != 12:
        end_month = datetime.strptime(f'{year}-{month + 1}-01', '%Y-%m-%d') - timedelta(days=1)
    else:
        end_month = datetime.strptime(f'{year + 1}-01-01', '%Y-%m-%d') - timedelta(days=1)

    if data.empty:
        return {}

    data['Дата платежа'] = pd.to_datetime(data['Дата платежа'], dayfirst=True)
    filtered_df_by_data = data[(data['Дата платежа'].between(start_month, end_month, inclusive='both'))]
    group_data = filtered_df_by_data.groupby('Категория').sum('Кэшбэк')
    sort_data = group_data.sort_values(by='Кэшбэк', ascending=False)
    result = {}
    for index, row in sort_data.head(3).iterrows():
        result[index] = float(row['Кэшбэк'])
    return json.dumps(result, ensure_ascii=False)


if __name__ == '__main__':
    data = get_data_from_excel(os.path.join(os.getenv("PATH_TO_DATA"), "test.xlsx"))
    pprint(analysis_categories_cashback(data, 2021, 12), indent=4)
