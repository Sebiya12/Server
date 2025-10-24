from abc import ABC, abstractmethod

class Tariff(ABC):
    """Абстрактный тариф мобильной связи"""

    def __init__(self, name: str, monthly_fee: int, minutes: int, data_gb: float, sms: int):
        self._name = name
        self._monthly_fee = monthly_fee
        self._minutes = minutes
        self._data_gb = data_gb
        self._sms = sms

    @property
    def name(self): return self._name

    @property
    def monthly_fee(self): return self._monthly_fee

    @property
    def minutes(self): return self._minutes

    @property
    def data_gb(self): return self._data_gb

    @property
    def sms(self): return self._sms

    def cost_per_gb(self):
        if self._data_gb == 0:
            return float("inf")
        return round(self._monthly_fee / self._data_gb, 2)

    @abstractmethod
    def type_name(self): ...

    def __str__(self):
        return f"{self._name} [{self.type_name()}]: {self._monthly_fee}₽/мес, {self._minutes} мин, {self._data_gb} ГБ, {self._sms} SMS"


class PrepaidTariff(Tariff):
    """Предоплатный тариф"""
    def __init__(self, name, monthly_fee, minutes, data_gb, sms, validity_days):
        super().__init__(name, monthly_fee, minutes, data_gb, sms)
        self._validity_days = validity_days

    def type_name(self): return "Prepaid"

    def __str__(self):
        return f"{super().__str__()}, срок действия {self._validity_days} дн."


class PostpaidTariff(Tariff):
    """Постоплатный тариф"""
    def __init__(self, name, monthly_fee, minutes, data_gb, sms, roaming_included):
        super().__init__(name, monthly_fee, minutes, data_gb, sms)
        self._roaming_included = roaming_included

    def type_name(self): return "Postpaid"

    def __str__(self):
        return f"{super().__str__()}, роуминг={'включён' if self._roaming_included else 'нет'}"


class UnlimitedTariff(Tariff):
    """Безлимитный тариф"""
    def __init__(self, name, monthly_fee, minutes, sms):
        super().__init__(name, monthly_fee, minutes, float("inf"), sms)

    def type_name(self): return "Unlimited"

    def __str__(self):
        return f"{super().__str__()} (безлимитный интернет)"


class MobileCompany:
    def __init__(self, name):
        self._name = name
        self._tariffs = []

    def add(self, tariff: Tariff):
        self._tariffs.append(tariff)

    def tariffs(self): return list(self._tariffs)

    def total_clients(self):
        return len(self._tariffs)

    def total_average_fee(self):
        if not self._tariffs:
            return 0
        return round(sum(t.monthly_fee for t in self._tariffs) / len(self._tariffs), 2)

    def sort_by(self, key_func):
        self._tariffs.sort(key=key_func)

    def find_by_fee_range(self, min_fee, max_fee):
        return [t for t in self._tariffs if min_fee <= t.monthly_fee <= max_fee]


def by_name(t): return t.name.lower()
def by_fee(t): return t.monthly_fee
def by_data(t): return t.data_gb
def by_cost_per_gb(t): return t.cost_per_gb()

def print_tariffs(company):
    if not company.tariffs():
        print("Список тарифов пуст.")
        return
    for i, t in enumerate(company.tariffs(), start=1):
        print(f"{i}) {t} | цена за 1 ГБ ≈ {t.cost_per_gb()}₽")


def menu():
    company = MobileCompany("Sebika Mobile")

    company.add(PrepaidTariff("Старт", 199, 200, 5, 50, 30))
    company.add(PostpaidTariff("Оптимум", 399, 600, 25, 200, True))
    company.add(UnlimitedTariff("Безлимит PRO", 699, 1200, 500))
    company.add(PostpaidTariff("Эконом", 249, 300, 10, 100, False))
    company.add(PrepaidTariff("Лайт", 149, 100, 3, 30, 15))

    print(f"Загружено {len(company.tariffs())} тарифов компании {company._name}")

    while True:
        print("\nМеню:")
        print("1) Показать все тарифы")
        print("2) Средняя абонентская плата")
        print("3) Сортировать тарифы")
        print("4) Найти тарифы по диапазону абонплаты")
        print("0) Выход")
        choice = input("Выбор: ").strip()

        if choice == "1":
            print_tariffs(company)
        elif choice == "2":
            print(f"Средняя абонентская плата: {company.total_average_fee()}₽")
        elif choice == "3":
            sort_opts = {
                "1": ("названию", by_name),
                "2": ("цене", by_fee),
                "3": ("объёму данных", by_data),
                "4": ("цене за 1 ГБ", by_cost_per_gb),
            }
            print("1) Названию\n2) Цене\n3) Объёму данных\n4) Цене за 1 ГБ")
            s = input("Выбор: ").strip()
            if s in sort_opts:
                text, func = sort_opts[s]
                company.sort_by(func)
                print(f"Отсортировано по {text}:")
                print_tariffs(company)
            else:
                print("Неверный выбор.")
        elif choice == "4":
            try:
                min_fee = int(input("Мин. абонплата (₽): "))
                max_fee = int(input("Макс. абонплата (₽): "))
                found = company.find_by_fee_range(min_fee, max_fee)
                if not found:
                    print("Ничего не найдено.")
                else:
                    for i, t in enumerate(found, start=1):
                        print(f"{i}) {t}")
            except ValueError:
                print("Ошибка ввода.")
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    print("=== Консольное приложение: Мобильная связь ===")
    menu()
