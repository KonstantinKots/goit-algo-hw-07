#Бот помічник з додаванням ДР

from collections import UserDict

#базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

#клас для зберігання імені контакту
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

#клас для зберігання телефону, валідність 10
class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Not correct format number phone")
        super().__init__(value)

#клас для зберігання інформації про контакт, включаючи ім'я та список телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_num):
        self.phones.append(Phone(phone_num))
    
    def remove_phone(self, phone_num):
        phone_remove = self.find_phone(phone_num)
        if phone_remove:
            self.phones.remove(phone_remove)
        else:
            raise ValueError(f"Number {phone_num} not found")
         
    def edit_phone(self, phone_num, new_phone):
        phone = self.find_phone(phone_num)
        if phone is None:
            raise ValueError(f"Phone {phone_num} not found")
        index = self.phones.index(phone)
        self.phones[index] = Phone(new_phone)
    
    def find_phone(self, phone_num):
        return next((p for p in self.phones if p.value == phone_num), None)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

#клас для зберігання та управління записами
class AddressBook(UserDict):
    def __init__(self, data = None):
        super().__init__(data)
    
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        return self.data.pop(name, None) 

    def __str__(self) -> str:
        return f"\n" .join(str(record) for record in self.data.values())

book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")