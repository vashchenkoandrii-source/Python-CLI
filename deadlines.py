from datetime import datetime, date
def validate_deadline(value):
    if value is None:
        return None
    try:
        parsed_date = datetime.strptime(value, "%d.%m.%Y")
        return parsed_date.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError("Неправильна дата. Використовуйте формат ДД.ММ.РРРР.")
def is_overdue(task):
    if not task["deadline"] or task["completed"]:
        return False
    deadline = datetime.strptime(task["deadline"], "%d.%m.%Y").date()
    return deadline < date.today()
def sort_tasks(tasks):
    def sort_key(task):
        if task["completed"]:
            return (2, date.max)
        if not task["deadline"]:
            return (1, date.max)
        deadline = datetime.strptime(task["deadline"], "%d.%m.%Y").date()
        return (0, deadline)
    return sorted(tasks, key=sort_key)