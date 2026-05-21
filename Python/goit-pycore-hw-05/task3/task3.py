import sys
from collections import defaultdict


def parse_log_line(line: str) -> dict:
    """
    Парсить один рядок логу та повертає словник.
    """
    parts = line.strip().split(" ", 3)

    if len(parts) < 4:
        return {}

    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2],
        "message": parts[3]
    }


def load_logs(file_path: str) -> list:
    logs = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parsed_line = parse_log_line(line)

                if parsed_line:
                    logs.append(parsed_line)

    except FileNotFoundError:
        print("Помилка: файл не знайдено.")
    
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    level = level.upper()

    return list(filter(
        lambda log: log["level"] == level,
        logs
    ))


def count_logs_by_level(logs: list) -> dict:
    counts = defaultdict(int)

    for log in logs:
        counts[log["level"]] += 1

    return counts


def display_log_counts(counts: dict):
    print("Рівень логування | Кількість")
    print("-----------------|----------")

    for level, count in counts.items():
        print(f"{level:<16} | {count}")


def main():
    if len(sys.argv) < 2:
        print("Використання:")
        print("python main.py logfile.log [level]")
        return

    file_path = sys.argv[1]

    logs = load_logs(file_path)

    if not logs:
        return

    counts = count_logs_by_level(logs)

    display_log_counts(counts)

    if len(sys.argv) >= 3:
        level = sys.argv[2]

        filtered_logs = filter_logs_by_level(logs, level)

        print(f"\nДеталі логів для рівня '{level.upper()}':")

        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()