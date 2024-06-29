import os
from datetime import datetime
from pprint import pprint

from src.utils import get_data_from_excel
from src.views import get_greeting, get_all_expenses, get_top_n_transactions, get_exchange_rates, get_stocks_prices
from dotenv import load_dotenv

load_dotenv()
PATH_TO_DATA = os.getenv("PATH_TO_DATA")


def main_views() -> None:
    """Функция реализует весь функционал модуля views.py"""

    df = get_data_from_excel(os.path.join(PATH_TO_DATA, "operations.xlsx"))
    result = {
        "greeting": get_greeting(datetime.today().strftime("%d-%m-%Y %H:%M:%S")),
        "cards": get_all_expenses(df),
        "top_transactions": get_top_n_transactions(df, date="30.06.2021 16:44:00", n=5),
        "currency_rates": get_exchange_rates(),
        "stock_prices": get_stocks_prices()
    }
    pprint(result, indent=4, sort_dicts=False)


if __name__ == "__main__":
    main_views()
