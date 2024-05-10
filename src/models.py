from consts import DATABASE_PATH


class Record:
    def __init__(self, date, category, amount, info):
        self.date = date
        self.category = category
        self.amount = amount
        self.info = info

    def update_date(self, new_date):
        self.date = new_date

    def update_category(self, new_category):
        self.category = new_category

    def update_amount(self, new_amount):
        self.amount = new_amount

    def update_info(self, new_info):
        self.info = new_info

    def save_to_db(self):
        with open(DATABASE_PATH, "a") as file:
            file.write(str(self) + "\n")

    def __repr__(self):
        return (
            f"Дата: {self.date}, "
            f"Категория: {self.category}, "
            f"Сумма: {self.amount}, "
            f"Описание: {self.info},"
        )
