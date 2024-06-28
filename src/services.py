import json
import os
from datetime import datetime, timedelta
from pprint import pprint
from typing import Any, Dict, List

import pandas as pd

from src.logger import setup_logging
from src.utils import get_data_from_excel

logger = setup_logging(f'services.py - {datetime.today().strftime("%Y-%m-%d")}')


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
    return round(result - amount, 2)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Принимает месяц ('YYYY-MM'), список словарей и предел, до которого нужно округлять суммы операций.
    Возвращает сумму, которую удалось бы отложить в «Инвесткопилку»."""
    all_amount = 0
    start = get_start_end_month(f"{month}-01")[0]
    end = get_start_end_month(f"{month}-01")[1]
    for transaction in transactions:
        date = datetime.strptime(transaction.get("Дата операции"), "%Y-%m-%d")

        if start <= date <= end:
            all_amount += round(round_to_limit(transaction.get("Сумма операции"), limit),2)
    logger.info(f'С {start} по {end} удалось бы накопить {all_amount} руб.')
    return all_amount


if __name__ == "__main__":
    data = get_data_from_excel(os.path.join(os.getenv("PATH_TO_DATA"), "operations.xlsx"))
    transactions = transactions_from_df(data)
    analysis_categories_cashback(data, 2021, 10)
    pprint(investment_bank("2018-10", transactions, 50), indent=4)
    # print(get_start_end_month('2018-12-08'))
