#Бот помічник з додаванням ДР
from datetime import datetime, date, timedelta
from collections import UserDict

con_file = "addressbook.txt"

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if str(e):
                return str(e)
            return "Give me name and phone please."
        except KeyError:
            return "Give me correct name and phone please."
        except IndexError:
            return "Enter the argument for the command."
    return inner

# базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# клас для зберігання імені контакту
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

# клас для зберігання телефону, валідність 10
class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Not correct format number phone")
        super().__init__(value)

# клас для зберігання дня народження, з перевіркою коректності введених даних
class Birthday(Field):
    def __init__(self, value):
        clean_date = value.strip().replace("р.", "").replace(" ", "")
        try:
            
            birthday = datetime.strptime(clean_date, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        today = datetime.today().date()
        if birthday > today:
            raise ValueError("Birthday cannot be in the future.")
        if (today.year - birthday.year) > 100:
            raise ValueError("Invalid birth year.")
        super().__init__(birthday)
        
        
# клас для зберігання інформації про контакт, включаючи ім'я та список телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

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
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if self.birthday:
            result += f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
        return result

# клас для зберігання та управління записами
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

# функція парсингу командної сторки
@input_error
def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    massage = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        massage = "Contact added."
    if phone:
        record.add_phone(phone)
    return massage

@input_error
def add_birthday(args, book: AddressBook):
        name, birthday = args
        record = book.find(name)
        if record is None:
            return f"Birthday {name} not found."
        record.add_birthday(birthday)
        return f"Birthday {name} added"

# Оновлює телефон існуючого контакту у словнику contacts.
@input_error
def change_contact(args: list, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if name in book:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError

#Пошук телефону за ім'ям у словнику contacts.
@input_error    
def show_phone(args: list, book: AddressBook):
    name = args[0].strip()
    return str(book.find(name))

# Виводить всі контакти зі словника contacts
def show_all(book: AddressBook):
    return str(book)

# Записує адресну книгу у текстовий файл.
def save_books(book: AddressBook):
    with open(con_file, 'w', encoding='utf-8') as file:
        for name, record in book.items():
            phone = record.phones[0].value if record.phones else "None"
            birthday = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "None"
            file.write(f"{name}:{phone}:{birthday}\n")

# Зчитує контактні данні з текстового файлу.
def read_contact_file():
    book = AddressBook()
    try:
        with open(con_file, 'r', encoding='utf-8') as file:
            for line in file:
                if not line or ":" not in line:
                    continue
                part = line.split(":", 2)
                while len(part) < 3:
                    part.append("")

                name, phone, birthday = part

                record = Record(name.strip())
                if phone and phone != "None":
                    record.add_phone(phone.strip())
                if birthday and birthday != "None":
                    record.add_birthday(birthday.strip())
                book.add_record(record)
    except FileNotFoundError:
        return AddressBook()
    return book

def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        days_ahead = 0 - birthday.weekday() + 7
        return birthday + timedelta(days=days_ahead)
    return birthday

def get_upcoming_birthdays(book: AddressBook, days=7):
    upcoming_birthdays = []
    today = date.today()
    for record in book.values():
        if not record.birthday:
            continue
        birthday_this_year = record.birthday.value.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
    
        if 0 <= (birthday_this_year - today).days <= days:
            birthday_this_year = adjust_for_weekend(birthday_this_year)
            congratulation_date_str = date_to_string(birthday_this_year)
            upcoming_birthdays.append(f"{record.name.value}: {congratulation_date_str}")
    return upcoming_birthdays

def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name} birthday: {record.birthday.value.strftime("%d.%m.%Y")}"
    

def birthdays(book):
    cong_list = get_upcoming_birthdays(book)
    if not cong_list:
        return "No birthdays next week"
    return f"\n".join(cong_list)

def main():
    book = AddressBook()
    commands = '''
1) exit, close - to exit the application
2) add [name] [new phone] - to add a new contact
3) change [name] [new phone] - to change the contact
4) phone [name] - to print number phone
5) all - to print all numbers
6) add-birthday [name] [date of birth] - to add the date of birth by name
7) show-birthday [name] - to print birthday by name
8) birthdays - to print a list of users to congratulate next week
9) help - to print this menu
'''
    print("\nWelcome to the assistant bot!\n")
    print(commands)
    try:
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")
            
            elif command == "add":
                print(add_contact(args, book))
                
            elif command == "change":
                print(change_contact(args, book))

            elif command == "phone":
                print(show_phone(args, book))

            elif command == "all":
                print(show_all(book))

            elif command == "help":
                print(commands)

            elif command == "add-birthday":
                print(add_birthday(args, book))

            elif command == "show-birthday":
                print(show_birthday(args, book))

            elif command == "birthdays":
                print(birthdays(book))

            else:
                print("Invalid command.")
    finally:
        save_books(book)
        print("AddressBook successfully saved")

if __name__ == "__main__":
    main()
