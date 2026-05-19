import random


def get_numbers_str(lottery_numbers: list) -> str:
    if not lottery_numbers:
        return "Error: Bad params"

    return str(lottery_numbers)


def get_numbers_ticket(min_val: int, max_val: int, quantity: int) -> list:
    if min_val > max_val:
        min_val, max_val = max_val, min_val

    total_available = max_val - min_val + 1

    if min_val < 1 or max_val > 1000 or quantity <= 0 or quantity > total_available:
        return []

    sampled_numbers = random.sample(range(min_val, max_val + 1), quantity)

    return sorted(sampled_numbers)


print("Your tickets:", get_numbers_str(get_numbers_ticket(1, 49, 6)))
print("Your tickets:", get_numbers_str(get_numbers_ticket(50, 1, 10)))
print("Your tickets:", get_numbers_str(get_numbers_ticket(1, 49, 1001)))
