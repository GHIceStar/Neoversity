def parse_input(user_input):
    parts = user_input.strip().split()

    if not parts:
        return "", []

    return parts[0].lower(), parts[1:]


def add_contact(args, contacts):
    if len(args) != 2:
        return "Invalid command."

    name, phone = args
    contacts[name] = phone

    return "Contact added."


def change_contact(args, contacts):
    if len(args) != 2:
        return "Invalid command."

    name, phone = args

    if name not in contacts:
        return "Contact not found."

    contacts[name] = phone

    return "Contact updated."


def show_phone(args, contacts):
    if len(args) != 1:
        return "Invalid command."

    name = args[0]

    if name not in contacts:
        return "Contact not found."

    return contacts[name]


def show_all(args, contacts):
    if not contacts:
        return "No contacts found."

    return "\n".join(
        f"{name}: {phone}"
        for name, phone in contacts.items()
    )


def main():
    contacts = {}

    handlers = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
    }

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")
            continue

        handler = handlers.get(command)

        if handler is None:
            print("Invalid command.")
            continue

        print(handler(args, contacts))


if __name__ == "__main__":
    main()