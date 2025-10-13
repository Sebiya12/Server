class Customer:
    def __init__(self, customer_id, last_name, first_name, patronymic, address, credit_card_number, bank_account_number):
        self.customer_id = customer_id  
        self.last_name = last_name  
        self.first_name = first_name  
        self.patronymic = patronymic  
        self.address = address  
        self.credit_card_number = credit_card_number  
        self.bank_account_number = bank_account_number  

    def set_attr(self, attr_name, value):
        if hasattr(self, attr_name):
            setattr(self, attr_name, value)
        else:
            raise AttributeError(f"У клиента нет атрибута '{attr_name}'")

    def get_attr(self, attr_name):
        if hasattr(self, attr_name):  
            return getattr(self, attr_name)
        else:
            raise AttributeError(f"У клиента нет атрибута '{attr_name}'")


    def __str__(self):
        return (f'Customer(id={self.customer_id}, last_name={self.last_name}, first_name={self.first_name}, '
                f'patronymic={self.patronymic}, address={self.address}, '
                f'credit_card_number={self.credit_card_number}, bank_account_number={self.bank_account_number})')

    def __hash__(self):
        return hash((self.customer_id, self.credit_card_number))

def filter_customers(customers, criteria):
    return [customer for customer in customers if criteria(customer)]

def alphabetical_order_criteria():
    return lambda customer: (customer.last_name, customer.first_name, customer.patronymic)

def credit_card_range_criteria(min_card_number, max_card_number):
    return lambda customer: min_card_number <= customer.credit_card_number <= max_card_number


customers = [
    Customer(1, "Байбуртли", "Себия", "Аметовна", "Симферополь, ул. Нижний квартал, 115", 1234567890123456, "RU123456789012345678"),
    Customer(2, "Бултов", "Азим", "Энверович", "Симферополь, ул. Беспалова, 3", 2345678901234567, "RU123456789012345679"),
    Customer(3, "Куриленко", "Максим", "Андреевич", "Симферополь, ул. Московская, 7", 3456789012345678, "RU123456789012345680"),
    Customer(4, "Гетьман", "Владислав", "Сергеевич", "Керчь, ул. Мирная, 11", 4567890123456789, "RU123456789012345681"),
    Customer(5, "Аблякимова", "Динара", "Наримановна", "Симферополь, ул. Акимова, 10", 5678901234567890, "RU123456789012345682"),
]
customers[0].set_attr("first_name", "Диана")

print("Список покупателей в алфавитном порядке:")
for customer in sorted(customers, key=alphabetical_order_criteria()):
    print(customer)


min_card = 2345678901234567
max_card = 4567890123456789
print(f"\nПокупатели с номерами кредитных карточек в диапазоне {min_card} - {max_card}:")
for customer in filter_customers(customers, credit_card_range_criteria(min_card, max_card)):
    print(customer)
