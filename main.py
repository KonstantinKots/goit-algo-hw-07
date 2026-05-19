#Бот помічник з додаванням ДР
from datetime import datetime, date, timedelta
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
#клас для зберігання дня народження, з перевіркою коректності введених даних
class Birthday(Field):
    def __init__(self, value):
        clean_date = value.strip().replace("р.", "").replace(" ", "")
        try:
            today = datetime.date.today()
            value = 

        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

#клас для зберігання інформації про контакт, включаючи ім'я та список телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.birthday = Birthday(birthday)

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
    
    def add_birthday(args, book):
        self.birthday = datetime(data_b) #rework

    def show_birthday(args, book):
        pass

    def birthdays(args, book):
        pass

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
    
#функція парсингу командної сторки
@input_error
def parse_input(user_input: str):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()

def date_to_string(date):
    return date.strftime("%Y.%m.%d")

def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": string_to_date(user["birthday"])})
    return prepared_list

def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday

def get_upcoming_birthdays(users, days=7):
    upcoming_birthdays = []
    today = date.today()

    for user in users:
        birthday_this_year = user["birthday"].replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
    
        if 0 <= (birthday_this_year - today).days <= days:
            birthday_this_year = adjust_for_weekend(birthday_this_year)
        congratulation_date_str = date_to_string(birthday_this_year)
        upcoming_birthdays.append({"name": user["name"], "congratulation_date": congratulation_date_str})
    return upcoming_birthdays

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
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_books(book)
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
            # реалізація

        elif command == "show-birthday":
            # реалізація

        elif command == "birthdays":
            # реалізація

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
