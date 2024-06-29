import os
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv

from src.logger import setup_logging
from src.utils import currency_exchange_rate, get_beginning_month, get_stock_price

load_dotenv()
PATH_TO_DATA = os.getenv("PATH_TO_DATA")
logger = setup_logging(f'views.py - {datetime.today().strftime("%Y-%m-%d")}')


def get_greeting(date: str) -> str:
    """Принимает строку с датой и временем в формате (dd-mm-YYYY HH:MM:SS),
    возвращает приветствие: «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»"""
    hour = int(date.split()[1].split(":")[0])
    minute = int(date.split()[1].split(":")[1])
    greeting = ""
    if hour in range(0, 6):
        greeting = "Доброй ночи"
    elif hour in range(6, 12):
        greeting = "Доброе утро"
    elif hour in range(12, 18):
        greeting = "Добрый день"
    elif hour in range(18, 24):
        greeting = "Добрый вечер"
    logger.info(f"get_greeting - Выбрано время {hour}:{minute} это {greeting.split()[1]}")
    return greeting


def get_all_expenses(df: pd.DataFrame) -> list[dict]:
    """Принимает DataFrame с банковскими операциями, возвращает список словарей,
    подсчитывает все расходы по карте и кешбэк"""
    if df.empty:
        return []
    expenses = df.loc[df["Сумма платежа"] < 0].groupby("Номер карты").agg({"Сумма операции": "sum"})
    result = []
    dict_data = expenses.to_dict().get("Сумма операции")
    for key, item in dict_data.items():
        result.append({"last_digits": key[-4:], "total_spent": item * -1, "cashback": round(item / -100, 2)})
        logger.info(f"get_all_expenses - По карте: {key[-4:]}, расходы: {item}, кешбэк: {round(item / -100, 2)}")

    return result


def get_top_n_transactions(df: pd.DataFrame, is_debit=None, date=None, n: int = 5) -> list[dict]:
    """Принимает DataFrame с банковскими операциями и дату, возвращает список словарей,
    top n транзакций по сумме платежа, с начала месяца по переданную дату."""

    if is_debit is None:
        is_debit = False

    if date is None:
        logger.info("Выбрана текущая дата")
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        beginning = get_beginning_month(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        beginning = pd.to_datetime(beginning, dayfirst=True)
        date = pd.to_datetime(date, dayfirst=True)
    else:
        try:
            beginning = pd.to_datetime(get_beginning_month(date), dayfirst=True)
            date = pd.to_datetime(date, dayfirst=True)
        except Exception as ex:
            logger.warning(f"Не верный формат даты {ex}")
            return []
    if df.empty:
        logger.warning("get_top_n_transactions - DataFrame пуст!")
        return []

    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    filtered_df_by_data = df[(df["Дата платежа"].between(beginning, date))]
    logger.info(f"Получены данные за период с {beginning} по {date}")
    pd.options.mode.chained_assignment = None  # Подавляем предупреждение SettingWithCopyWarning
    filtered_df_by_data["Дата платежа"] = filtered_df_by_data["Дата платежа"].dt.strftime("%d.%m.%Y")
    if is_debit:
        logger.info('Выбран режим: "Доходы"')
        filtered_by_payment = filtered_df_by_data.loc[filtered_df_by_data["Сумма платежа"] > 0]
    else:
        logger.info('Выбран режим: "Расходы"')
        filtered_by_payment = filtered_df_by_data.loc[filtered_df_by_data["Сумма платежа"] < 0]

    top_n = filtered_by_payment.sort_values(by="Сумма платежа", ascending=False).head(n).to_dict(orient="records")
    logger.info("Данные отсортированы по Сумме платежа")

    result = []
    for item in top_n:
        result.append(
            {
                "date": item.get("Дата платежа"),
                "amount": item.get("Сумма платежа"),
                "category": item.get("Категория"),
                "description": item.get("Описание"),
            }
        )
    logger.info(f"Получено Top - {n} транзакций за период с {beginning} по {date}")
    return result


def get_exchange_rates(currencies: list = None) -> list[dict]:
    """Принимает список валют, возвращает список словарей с курсами валют"""

    if currencies is None:
        currencies = ["USD", "EUR"]
    result = []
    for currency in currencies:
        result.append({"currency": currency, "rate": round(currency_exchange_rate(currency), 2)})
        logger.info("Сформированы данные с курсами валют")

    return result


def get_stocks_prices(stocks: list = None) -> list[dict]:
    """Принимает список акций, возвращает список словарей с ценами акций"""

    if stocks is None:
        stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    result = []
    for stock in stocks:
        price = get_stock_price(stock)
        result.append({"stock": stock, "price": price})
        logger.info(f"Курс акции {stock} - {price}")
    return result
