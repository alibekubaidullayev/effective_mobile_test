import re
import datetime
from db_parser import read_db, save_to_db
from models import Record


def get_input(prompt, valid_check, error_message):
    """
    Проверяет вводимые пользователем данные в зависимости от их типа.
    """
    while True:
        value = input(prompt)
        if valid_check(value):
            return value
        print(error_message)


def parse_input(input_str, pattern):
    """
    Парсит данные для поиска по дате или сумме.
    Преобразует данные к нужному типу и возвращает кортеж с оператором и значением.
    """
    match = re.match(pattern, input_str)
    if match:
        operator, value = match.groups()
        if pattern == r"([<>=]*)(\d{4}-\d{2}-\d{2})":
            try:
                value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                return None
        elif pattern == r"([<>=]*)(\d+)":
            value = int(value)
        return (operator, value)
    return None


def matches_criteria(record_value, input_str, value_type):
    """
    Применяет правильный шаблон к данным и получает оператор и значение.
    Затем сравнивает значение записи с входным значением.
    """
    pattern = (
        r"([<>=]*)(\d{4}-\d{2}-\d{2})" if value_type == "date" else r"([<>=]*)(\d+)"
    )
    result = parse_input(input_str, pattern)
    if result:
        operator, value = result
        if value_type == "date":
            if isinstance(record_value, str):
                record_value = datetime.datetime.strptime(
                    record_value, "%Y-%m-%d"
                ).date()
        else:
            record_value = int(record_value)
        if operator == "<":
            return record_value < value
        elif operator == "<=":
            return record_value <= value
        elif operator == ">":
            return record_value > value
        elif operator == ">=":
            return record_value >= value
        elif operator == "=" or operator == "":
            return record_value == value
    return False


"""
Ниже идут функции для каждого пункта меню.
Функции довольно интуитивные и не нуждаются в дополнительных комментариях.
"""


def main_menu():
    print("[1] Баланс")
    print("[2] Добавить Запись")
    print("[3] Редактировать Запись")
    print("[4] Поиск Записи")
    print("[q] Выход")
    return input("Выберите опцию: ")


def balance_menu():
    records = read_db()
    total = 0
    for r in records:
        if r.category == "Expense":
            total -= int(r.amount)
        else:
            total += int(r.amount)
    print(f"Баланс: {total}")
    input("Нажмите Enter для возврата...")
    return "main_menu"


def add_record_menu():
    print("Добавление Записи...")
    new_category = get_input(
        "Введите категорию {Income, Expense}: ",
        lambda x: x in ["Income", "Expense"],
        "Неверная категория, попробуйте еще раз.",
    )
    new_amount = get_input(
        "Введите сумму: ",
        lambda x: x.isdigit(),
        "Неверная сумма, попробуйте еще раз.",
    )
    new_info = get_input(
        "Введите информацию: ",
        lambda x: x or not x,
        "Неверная информация, попробуйте еще раз.",
    )
    date = datetime.date.today().strftime("%Y-%m-%d")
    record = Record(date, new_category, new_amount, new_info)
    record.save_to_db()
    input("Нажмите Enter для возврата...")
    return "main_menu"


def edit_record_menu():
    print("Редактирование Записи...")
    records = read_db()
    for i, r in enumerate(records):
        print(f"[{i+1}]", r)
    record_id = get_input(
        "Выберите запись для редактирования: ",
        lambda x: x.isdigit() and 0 < int(x) <= len(records),
        "Неверный номер записи, попробуйте еще раз.",
    )
    record_id = int(record_id) - 1
    new_category = get_input(
        "Введите новую категорию {Income, Expense} (нажмите Enter, чтобы пропустить): ",
        lambda x: not x or x in ["Income", "Expense"],
        "Неверная категория, попробуйте еще раз.",
    )
    new_amount = get_input(
        "Введите новую сумму (нажмите Enter, чтобы пропустить): ",
        lambda x: not x or x.isdigit(),
        "Неверная сумма, попробуйте еще раз.",
    )
    new_info = get_input(
        "Введите новую информацию (нажмите Enter, чтобы пропустить): ",
        lambda x: x or not x,
        "Неверная информация, попробуйте еще раз.",
    )
    if new_category:
        records[record_id].category = new_category
    if new_amount:
        records[record_id].amount = new_amount
    if new_info:
        records[record_id].info = new_info

    try:
        save_to_db(records)
        print("Запись успешно обновлена!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    input("Нажмите Enter для возврата...")
    return "main_menu"


def search_record_menu():
    print("Фильтры поиска: <=, <, >, >=, =")
    date_search = get_input(
        "Введите дату для поиска (например, <=2024-02-05) или нажмите Enter для пропуска: ",
        lambda x: not x or parse_input(x, r"([<>=]*)(\d{4}-\d{2}-\d{2})"),
        "Неверная дата, используйте операторы вида <, <=, >, >=, =, за которыми следует YYYY-MM-DD.",
    )
    category_search = get_input(
        "Введите категорию для поиска {Income, Expense} или нажмите Enter для пропуска: ",
        lambda x: not x or x in ["Income", "Expense"],
        "Неверная категория, попробуйте еще раз.",
    )
    amount_search = get_input(
        "Введите сумму для поиска (например, >500) или нажмите Enter для пропуска: ",
        lambda x: not x or parse_input(x, r"([<>=]*)(\d+)"),
        "Неверная сумма, используйте операторы вида <, <=, >, >=, =, за которыми следует целое число.",
    )
    info_search = get_input(
        "Введите информацию для поиска или нажмите Enter для пропуска: ",
        lambda x: x or not x,
        "Неверная информация, попробуйте еще раз.",
    )
    records = read_db()
    filtered_records = [
        r
        for r in records
        if (not date_search or matches_criteria(r.date, date_search, "date"))
        and (not category_search or r.category == category_search)
        and (not amount_search or matches_criteria(r.amount, amount_search, "amount"))
        and (not info_search or info_search.lower() in r.info.lower())
    ]
    if filtered_records:
        print("Результаты Поиска:")
        for r in filtered_records:
            print(r)
    else:
        print("Записи, соответствующие критериям, не найдены.")
    input("Нажмите Enter для возврата...")
    return "main_menu"
