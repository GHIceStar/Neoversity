import re


def normalize_phone(phone_number: str) -> str:
    cleaned = re.sub(r"\D", "", phone_number)

    if cleaned.startswith("380"):
        return f"+{cleaned}"
    
    elif cleaned.startswith("0"):
        return f"+38{cleaned}"
    
    return f"+{cleaned}" if cleaned else ""

raw_numbers = [
    "067\t123 4567",
    "(095) 234-5678\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]

print("Phone numbers:")
print(sanitized_numbers)