from datetime import datetime

def get_days_from_today(date: str) -> int:
    try:
        given_date = datetime.strptime(date, "%Y-%m-%d").date()
        today_date = datetime.today().date()
        delta = today_date - given_date
        return delta.days
        
    except ValueError:
        print(f"Error: '{date}' bad format YYYY MM DDD")
        return None

print(get_days_from_today("2026-05-20"))
print(get_days_from_today("2026-05-10"))
print(get_days_from_today("2026/05/10"))
print(get_days_from_today("some text"))