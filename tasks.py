from storage import load_Hello, save_Hello
from deadlines import validate_deadline, is_overdue, sort_tasks
def add_task(text, deadline=None):
    text = text.strip()
    if not text:
        raise ValueError("Назва завдання не може бути порожньою.")
    deadline = validate_deadline(deadline)
    Hello = load_Hello()
    new_id = max((task["id"] for task in Hello), default=0) + 1
    Hello.append({
        "id": new_id,
        "text": text,
        "deadline": deadline,
        "completed": False
    })
    save_Hello(Hello)
    print(f"Завдання №{new_id} успішно додано.")
def show_tasks():
    Hello = load_Hello()
    if not Hello:
        print("Список завдань порожній.")
        return
    overdue = []
    active = []
    completed = []
    for task in sort_tasks(Hello):
        if task["completed"]:
            completed.append(task)
        elif is_overdue(task):
            overdue.append(task)
        else:
            active.append(task)
    def print_group(title, tasks):
        print(f"\n{title}")
        if not tasks:
            print("Немає завдань.")
            return
        for task in tasks:
            deadline = task["deadline"] or "Не встановлено"
            print(f'[{task["id"]}] {task["text"]} | Дедлайн: {deadline}')
    print_group("ПРОСТРОЧЕНІ ЗАВДАННЯ", overdue)
    print_group("АКТИВНІ ЗАВДАННЯ", active)
    print_group("ВИКОНАНІ ЗАВДАННЯ", completed)
def edit_task(task_id, text=None, deadline=None, clear_deadline=False):
    Hello = load_Hello()
    for task in Hello:
        if task["id"] == task_id:
            if text is not None:
                text = text.strip()
                if not text:
                    raise ValueError("Назва завдання не може бути порожньою.")
                task["text"] = text
            if clear_deadline:
                task["deadline"] = None
            elif deadline is not None:
                task["deadline"] = validate_deadline(deadline)
            save_Hello(Hello)
            print(f"Завдання №{task_id} успішно змінено.")
            return
    raise ValueError(f"Завдання №{task_id} не знайдено.")
def delete_task(task_id):
    Hello = load_Hello()
    for task in Hello:
        if task["id"] == task_id:
            Hello.remove(task)
            save_Hello(Hello)
            print(f"Завдання №{task_id} видалено.")
            return
    raise ValueError(f"Завдання №{task_id} не знайдено.")
def complete_task(task_id):
    Hello = load_Hello()
    for task in Hello:
        if task["id"] == task_id:
            task["completed"] = True
            save_Hello(Hello)
            print(f"Завдання №{task_id} позначено як виконане.")
            return
    raise ValueError(f"Завдання №{task_id} не знайдено.")
def show_stats():
    Hello = load_Hello()
    total = len(Hello)
    completed = sum(task["completed"] for task in Hello)
    overdue = sum(is_overdue(task) for task in Hello)
    active = total - completed
    print(f"Усього завдань: {total}")
    print(f"Активних завдань: {active}")
    print(f"Виконаних завдань: {completed}")
    print(f"Прострочених завдань: {overdue}")
def clear_tasks():
    save_Hello([])
    print("Усі завдання видалено.")