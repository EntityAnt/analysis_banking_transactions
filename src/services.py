import json
import os
from datetime import datetime
from pprint import pprint
from typing import Any, Dict, List

import pandas as pd

from src.logger import setup_logging
from src.utils import get_data_from_excel, get_start_end_month, transactions_from_df, round_to_limit

logger = setup_logging(f'services.py - {datetime.today().strftime("%Y-%m-%d")}')


def analysis_categories_cashback(data: pd.DataFrame, year: int, month: int) -> json:
    """На вход функции поступают данные для анализа, год и месяц.
    На выходе — JSON с анализом, сколько на каждой категории можно заработать кешбэка в указанном месяце года."""

    start_month = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
    end_month = get_start_end_month(start_month.strftime("%Y-%m-%d"))[1]
    logger.info(f'Анализ кешбэка по категориям - выбран период: с {start_month} по {end_month}')
    if data.empty:
        logger.warning('Анализ кешбэка по категориям - DataFrame пуст!')
        return {}

    data["Дата платежа"] = pd.to_datetime(data["Дата платежа"], dayfirst=True)
    filtered_df_by_data = data[(data["Дата платежа"].between(start_month, end_month, inclusive="both"))]
    group_data = filtered_df_by_data.groupby("Категория").sum("Кэшбэк")
    sort_data = group_data.sort_values(by="Кэшбэк", ascending=False)
    result = {}
    for index, row in sort_data.head(3).iterrows():
        result[index] = float(row["Кэшбэк"])
        logger.info(f'{index}:  {float(row["Кэшбэк"])}')

    return json.dumps(result, ensure_ascii=False)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Принимает месяц ('YYYY-MM'), список словарей и предел, до которого нужно округлять суммы операций.
    Возвращает сумму, которую удалось бы отложить в «Инвесткопилку»."""
    all_amount = 0
    start = get_start_end_month(f"{month}-01")[0]
    end = get_start_end_month(f"{month}-01")[1]
    for transaction in transactions:
        date = datetime.strptime(transaction.get("Дата операции"), "%Y-%m-%d")

        if start <= date <= end:
            all_amount += round(round_to_limit(transaction.get("Сумма операции"), limit), 2)
    logger.info(f'С {start} по {end} удалось бы накопить {all_amount} руб.')
    return all_amount

df = get_data_from_excel(os.path.join(os.getenv('PATH_TO_DATA'), "operations.xlsx"))
transactions = transactions_from_df(df)
print(investment_bank('2021-11', transactions, 100))

