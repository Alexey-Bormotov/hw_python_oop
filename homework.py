import datetime as dt


class Record:
    """Класс для хранения записей."""
    # Формат для преобразования даты из строки
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        if type(date) == str:
            self.date = dt.datetime.strptime(date, self.date_format).date()


class Calculator:
    """Родительский класс калькуляторов."""
    # Текущая дата
    today = dt.datetime.now().date()

    def __init__(self, limit):
        self.limit = limit
        # Пустой список для хранения записей
        self.records = []

    def add_record(self, data):
        """Добавление записи в список."""
        self.records.append(data)

    def get_today_stats(self):
        """Подсчет статистики за сегодня."""
        sum = 0
        for record in self.records:
            if record.date == self.today:
                sum += record.amount
        return sum

    def get_week_stats(self):
        """Подсчет статистики за последние 7 дней."""
        # Дата неделю назад
        week_ago = self.today - dt.timedelta(days=7)
        sum = 0
        for record in self.records:
            if (record.date <= self.today) and (record.date > week_ago):
                sum += record.amount
        return sum


class CashCalculator(Calculator):
    """Калькулятор денег."""
    # Курсы валют
    USD_RATE = 72.72
    EURO_RATE = 86.4

    def get_today_cash_remained(self, currency):
        """Подсчет остатка средств на сегодня"""
        # Вычисляем остаток на сегодня
        diff = self.limit - self.get_today_stats()
        # Словарь для валют
        cur_dict = {
            'rub': 'руб',
            'usd': 'USD',
            'eur': 'Euro'
        }
        selected_cur = cur_dict[currency]

        # Преобразование валют
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
        else:
            return 'Денег нет, держись'


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
