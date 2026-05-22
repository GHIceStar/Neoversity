from collections import UserDict
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
        if not self.is_valid_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits")

        super().__init__(value)

    @classmethod
    def is_valid_phone(cls, value):
        return re.fullmatch(cls.PHONE_PATTERN, value) is not None


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError:
            print(f"Phone number '{phone}' is not correct. Use exactly 10 digits.")

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)

        if found_phone is None:
            raise ValueError("Phone number not found")

        self.phones.remove(found_phone)

    def edit_phone(self, old_phone, new_phone):
        found_phone = self.find_phone(old_phone)

        if found_phone is None:
            raise ValueError("Phone number not found")

        new_phone_object = Phone(new_phone)
        phone_index = self.phones.index(found_phone)
        self.phones[phone_index] = new_phone_object

    def find_phone(self, phone):
        for phone_object in self.phones:
            if phone_object.value == phone:
                return phone_object

        return None

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name not in self.data:
            raise KeyError("Contact not found")

        del self.data[name]


def main():
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_phone("5555555ff5")
    john_record.add_phone("555555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")


if __name__ == "__main__":
    main()