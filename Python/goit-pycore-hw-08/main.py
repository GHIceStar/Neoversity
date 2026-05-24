from collections import UserDict
from datetime import datetime, timedelta
import pickle
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    PHONE_PATTERN = r"^\d{10}$"

    def __init__(self, value):
        if not re.fullmatch(self.PHONE_PATTERN, value):
            raise ValueError(
                "Invalid phone number. Use exactly 10 digits."
            )

        super().__init__(value)


class Birthday(Field):
    BIRTHDAY_PATTERN = r"^\d{2}\.\d{2}\.\d{4}$"

    def __init__(self, value):
        if not re.fullmatch(self.BIRTHDAY_PATTERN, value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")

        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")

        super().__init__(birthday)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_object = self.find_phone(phone)

        if phone_object is None:
            raise ValueError("Phone number not found.")

        self.phones.remove(phone_object)

    def edit_phone(self, old_phone, new_phone):
        phone_object = self.find_phone(old_phone)

        if phone_object is None:
            raise ValueError("Old phone number not found.")

        phone_index = self.phones.index(phone_object)
        self.phones[phone_index] = Phone(new_phone)

    def find_phone(self, phone):
        for phone_object in self.phones:
            if phone_object.value == phone:
                return phone_object

        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def get_birthday(self):
        if self.birthday is None:
            return None

        return self.birthday.value.strftime("%d.%m.%Y")

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)

        if not phones:
            phones = "no phone numbers"

        birthday = self.get_birthday()

        if birthday is None:
            birthday = "not added"

        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones}, "
            f"birthday: {birthday}"
        )


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name not in self.data:
            raise KeyError("Contact not found.")

        del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        result = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            days_difference = (birthday_this_year - today).days

            if days_difference > 7:
                continue

            congratulation_date = self.get_congratulation_date(
                birthday_this_year
            )

            result.append(
                {
                    "name": record.name.value,
                    "congratulation_date": (
                        congratulation_date.strftime("%d.%m.%Y")
                    ),
                }
            )

        return result

    @staticmethod
    def get_congratulation_date(date):
        if date.weekday() == 5:
            return date + timedelta(days=2)

        if date.weekday() == 6:
            return date + timedelta(days=1)

        return date


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


def input_error(func):
    def wrapper(args, book):
        try:
            return func(args, book)
        except ValueError as error:
            return str(error)
        except KeyError as error:
            return str(error).strip("'")
        except IndexError:
            return "Not enough arguments."

    return wrapper


def parse_input(user_input):
    parts = user_input.strip().split()

    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


@input_error
def add_contact(args, book):
    name, phone = args

    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."

    record.add_phone(phone)

    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args

    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.edit_phone(old_phone, new_phone)

    return "Phone number changed."


@input_error
def show_phone(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        return "Contact not found."

    if not record.phones:
        return "This contact has no phone numbers."

    phones = "; ".join(phone.value for phone in record.phones)

    return f"{name}: {phones}"


@input_error
def show_all(args, book):
    if not book.data:
        return "Address book is empty."

    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    name, birthday = args

    record = book.find(name)

    if record is None:
        return "Contact not found."

    record.add_birthday(birthday)

    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        return "Contact not found."

    birthday = record.get_birthday()

    if birthday is None:
        return "Birthday not added."

    return f"{name}'s birthday: {birthday}"


@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()

    if not upcoming_birthdays:
        return "No upcoming birthdays."

    result = []

    for birthday_info in upcoming_birthdays:
        result.append(
            f"{birthday_info['name']}: "
            f"{birthday_info['congratulation_date']}"
        )

    return "\n".join(result)


def main():
    book = load_data()

    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
    }

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            save_data(book)
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")
            continue

        handler = commands.get(command)

        if handler is None:
            print("Invalid command.")
            continue

        print(handler(args, book))


if __name__ == "__main__":
    main()