import re

from models import Record
from consts import DATABASE_PATH, ENTRY_PATTERN


def read_db():
    """
    Считывает данные из .txt файла и превращает в Record объекты.
    """
    records = []
    with open(DATABASE_PATH, "r") as file:
        lines = file.readlines()

    entries_list = [re.findall(ENTRY_PATTERN, line) for line in lines]
    for entry in entries_list:
        if not len(entry):
            continue
        rec = Record(*entry)
        records.append(rec)

    return records


def save_to_db(records):
    with open(DATABASE_PATH, "w") as file:
        for record in records:
            file.write(str(record) + "\n")
