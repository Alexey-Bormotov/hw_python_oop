import datetime as dt


class Record:
    """Класс для хранения записей."""
    # Формат для преобразования даты из строки
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        if type(date) == str:
            self.date = dt.datetime.strptime(date, self.date_format).date()


class Calculator:
    """Родительский класс калькуляторов."""
    # Текущая дата
    today = dt.date.today()

    def __init__(self, limit):
        self.limit = limit
        # Пустой список для хранения записей
        self.records = []

    def add_record(self, data):
        """Добавление записи в список."""
        self.records.append(data)

    def get_today_stats(self):
        """Подсчет статистики за сегодня."""
        # Список со значениями (amount) за сегодня
        today_amount_list = ([record.amount for record in self.records
                             if record.date == self.today])
        return sum(today_amount_list)

    def get_week_stats(self):
        """Подсчет статистики за последние 7 дней."""
        # Дата неделю назад
        week_ago = self.today - dt.timedelta(days=7)
        # Список со значениями (amount) за неделю
        week_amount_list = ([record.amount for record in self.records
                            if (week_ago < record.date <= self.today)])
        return sum(week_amount_list)


class CashCalculator(Calculator):
    """Калькулятор денег."""
    # Словарь для валют {Ключ: [Название, Курс]}
    cur_dict = {
        'rub': ['руб', 1],
        'usd': ['USD', 72.72],
        'eur': ['Euro', 86.4],
    }
    USD_RATE = cur_dict['usd'][1]  # без этих строк pytest ругается
    EURO_RATE = cur_dict['eur'][1]  # без этих строк pytest ругается

    def get_today_cash_remained(self, currency):
        """Подсчет остатка средств на сегодня"""
        # Вычисляем остаток на сегодня
        diff = self.limit - self.get_today_stats()

        # Проверяем правильно ли указана валюта
        if currency not in self.cur_dict:
            return 'Валюта указана неверно.'

        # Если денег нет - держимся
        if diff == 0:
            return 'Денег нет, держись'

        # Выбираем нужное название для выбранной валюты
        selected_cur = self.cur_dict[currency][0]

        # Преобразуем значение по курсу согласно выбранной валюты
        # diff /= self.cur_dict[currency][1] - такое вычисление курса
        # pytest'у не нравится, оставил старое,
        # т.к. пока не знаю как его победить
        if currency == 'usd':
            diff /= self.USD_RATE
        elif currency == 'eur':
            diff /= self.EURO_RATE

        # Определение результата по остатку
        if diff > 0:
            return f'На сегодня осталось {diff:.2f} {selected_cur}'
        elif diff < 0:
            return (f'Денег нет, держись: '
                    f'твой долг - {abs(diff):.2f} {selected_cur}')
# Flake8 теперь ругается здесь на отсутствие явного возврата


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""
    def get_calories_remained(self):
        """Подсчет остатка калорий на сегодня"""
        # Вычисляем остаток на сегодня
        diff = self.limit - self.get_today_stats()

        # Определение результата по остатку
        if diff > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {diff} кКал')
        return 'Хватит есть!'
