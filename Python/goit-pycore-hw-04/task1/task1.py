from pathlib import Path


def total_salary(path: str):
    total = 0
    count = 0
    
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    _, salary = line.split(",")
                    total += int(salary)
                    count += 1
                except ValueError:
                    print(f"Попередження: рядок '{line}' має неправильний формат.")
                    continue
                    
        average = total / count if count > 0 else 0
        return (total, average)

    except FileNotFoundError:
        print(f"Помилка: файл за шляхом '{path}' не знайдено.")
        return (0, 0)
    except Exception as e:
        print(f"Сталася непередбачена помилка: {e}")
        return (0, 0)


result = total_salary(Path(__file__).parent / "salary_file.txt")
print(f"Загальна сума: {result[0]}, Середня: {result[1]}")