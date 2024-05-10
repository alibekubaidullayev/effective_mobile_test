import os
import sys
import time

from menus import (
    main_menu,
    balance_menu,
    add_record_menu,
    edit_record_menu,
    search_record_menu,
)

"""
Маппинг названий менюшек на функции
"""
STATE_FUNCTIONS = {
    "main_menu": main_menu,
    "balance_menu": balance_menu,
    "add_record_menu": add_record_menu,
    "edit_record_menu": edit_record_menu,
    "search_record_menu": search_record_menu,
}


def run_cli():
    """
    CLI выполнен в качестве цикла, который меняет менюшки
    и вызывает нужные функции в зависимости от выбора юзера.
    """

    state = "main_menu"
    while state != "quit":
        if os.name != "nt":
            sys.stdout.write("\0337")  # Строчка нужна чтобы сохранить позицию курсора
        time.sleep(0.1)
        if state == "main_menu":
            choice = STATE_FUNCTIONS[state]()  # Вызов нужной менюшки
            if choice == "1":
                state = "balance_menu"
            elif choice == "2":
                state = "add_record_menu"
            elif choice == "3":
                state = "edit_record_menu"
            elif choice == "4":
                state = "search_record_menu"
            elif choice == "q":
                state = "quit"
            else:
                print("Невалидная опция. Попробуйте еще раз")
                time.sleep(2)
        else:
            state = STATE_FUNCTIONS[state]()

        if os.name != "nt":
            sys.stdout.write("\0338\033[J")  # Востанавливает позицию курсора
            sys.stdout.flush()  # Очищает экран. Все это делается для динамичной картинки в терминале


if __name__ == "__main__":
    run_cli()
