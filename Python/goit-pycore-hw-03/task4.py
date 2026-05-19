from datetime import datetime, timedelta


def get_upcoming_birthdays(users):
    today = datetime.today().date()
    upcoming_birthdays = []
    
    weekend_shift = {5: 2, 6: 1}

    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        birthday_this_year = birthday.replace(year=today.year)
        
        if birthday_this_year < today:
            birthday_this_year = birthday.replace(year=today.year + 1)
        
        delta = (birthday_this_year - today).days
        if 0 <= delta <= 7:
            weekday = birthday_this_year.weekday()
            congratulation_date = birthday_this_year + timedelta(days=weekend_shift.get(weekday, 0))
            
            upcoming_birthdays.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })
            
    return upcoming_birthdays



users = [
    {"name": "John Doe", "birthday": "1985.05.19"},
    {"name": "Jane Smith", "birthday": "1990.05.23"},
    {"name": "Mike Ross", "birthday": "1988.05.24"},
    {"name": "Alice Wong", "birthday": "1992.05.21"},
    {"name": "Bob Builder", "birthday": "1980.05.28"},
    {"name": "Charlie Brown", "birthday": "1995.05.15"}
]

print(get_upcoming_birthdays(users))