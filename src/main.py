import os
from datetime import datetime
from pprint import pprint

from dotenv import load_dotenv

from src.logger import setup_logging
from src.reports import spending_by_category
from src.utils import get_data_from_excel, get_date_n_months_later, str_title

load_dotenv()
logger = setup_logging(f'main.py - {datetime.today().strftime("%Y-%m-%d")}')


def main_reports() -> None:
    """Функция реализует весь функционал модуля reports.py"""
    df = get_data_from_excel(os.path.join(os.getenv("PATH_TO_DATA"), "operations.xlsx"))
    print("Для формирования отчета")
    while True:
        date = input("Введите дату в формате dd.mm.YYYY: ").strip()
        try:
            year = datetime.strptime(date, "%d.%m.%Y").year
            if (year < 2018) or (year > 2021):
                print("Для анализа доступны данные с 2018 по 2021 года включительно!")
                continue
            break
        except ValueError as ex:
            logger.error(f"Ошибка: {ex}")
            print("Не верный формат даты!")
            continue

    while True:
        category = str_title(input("Ведите название категории: ").strip())
        filtered_by_category = df.loc[df["Категория"] == category]
        if filtered_by_category.empty:
            print("Такой категории не существует!")
            continue
        break
    report = spending_by_category(df, category, date).to_dict(orient="records")
    start_date = get_date_n_months_later(date, 3).strftime("%d.%m.%Y")
    print("*" * 50)
    print(f'Сформирован отчет: Траты по категории "{category}" с {start_date} по {date}')
    answer = input("Вывести отчет на экран (Да/Нет) ").lower().strip()
    if answer == "да":
        pprint(report, indent=4)
        print("*" * 50)
        print("Работа программы закончена, всего вам доброго.")
    else:
        print("*" * 50)
        print("Работа программы закончена, всего вам доброго.")


if __name__ == "__main__":
    main_reports()
