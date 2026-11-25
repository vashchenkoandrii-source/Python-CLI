import FreeSimpleGUI as sg
import json
import os
from datetime import datetime
FILE_NAME = "Hello.json"
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []
def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)
def format_task(task):
    text = task.get("text", "Без назви")
    deadline = task.get("deadline")
    completed = task.get("completed", False)
    if completed:
        status = "Виконано"
    elif deadline:
        try:
            date = datetime.strptime(deadline, "%d.%m.%Y")
            status = "Прострочено" if date.date() < datetime.now().date() else "У процесі"
        except ValueError:
            status = "У процесі"
    else:
        status = "У процесі"
    return f"{text} | Дедлайн: {deadline or 'Не встановлено'} | {status}"
def refresh(window):
    tasks = load_tasks()
    window["-TASKS-"].update(values=[
        format_task(task) for task in tasks
    ])
def add_task(window, values):
    text = values["-TEXT-"].strip()
    deadline = values["-DATE-"].strip()
    if not text:
        sg.popup_error("Введіть назву завдання!")
        return
    if deadline:
        try:
            datetime.strptime(deadline, "%d.%m.%Y")
        except ValueError:
            sg.popup_error("Неправильна дата! Формат: ДД.ММ.РРРР")
            return
    tasks = load_tasks()
    tasks.append({
        "text": text,
        "deadline": deadline if deadline else None,
        "completed": False
    })
    save_tasks(tasks)
    window["-TEXT-"].update("")
    window["-DATE-"].update("")
    refresh(window)
def get_selected(window):
    selected = window["-TASKS-"].get_indexes()
    if not selected:
        sg.popup_error("Виберіть завдання зі списку!")
        return None
    tasks = load_tasks()
    if selected[0] >= len(tasks):
        return None
    return selected[0]
def delete_task(window):
    index = get_selected(window)
    if index is None:
        return
    tasks = load_tasks()
    del tasks[index]
    save_tasks(tasks)
    refresh(window)
def complete_task(window):
    index = get_selected(window)
    if index is None:
        return
    tasks = load_tasks()
    tasks[index]["completed"] = True
    save_tasks(tasks)
    refresh(window)
def edit_task(window):
    index = get_selected(window)
    if index is None:
        return
    tasks = load_tasks()
    task = tasks[index]
    new_text = sg.popup_get_text(
        "Нова назва завдання:",
        default_text=task.get("text", "")
    )
    if new_text is None:
        return
    if not new_text.strip():
        sg.popup_error("Назва завдання не може бути порожньою!")
        return
    new_deadline = sg.popup_get_text(
        "Новий дедлайн (ДД.ММ.РРРР). Залиш порожнім, щоб прибрати дедлайн:",
        default_text=task.get("deadline") or ""
    )
    if new_deadline is None:
        return
    new_deadline = new_deadline.strip()
    if new_deadline:
        try:
            datetime.strptime(new_deadline, "%d.%m.%Y")
        except ValueError:
            sg.popup_error("Неправильна дата!")
            return
    task["text"] = new_text.strip()
    task["deadline"] = new_deadline if new_deadline else None
    save_tasks(tasks)
    refresh(window)
sg.theme("LightBlue3")
layout = [
    [sg.Text("TASKHUB", font=("Arial", 22, "bold"))],
    [sg.Text("Нове завдання:", size=(16, 1)), sg.Input(key="-TEXT-", expand_x=True)],
    [sg.Text("Дедлайн (ДД.ММ.РРРР):", size=(16, 1)), sg.Input(key="-DATE-", expand_x=True)],
    [sg.Button("Додати завдання", key="-ADD-")],
    [sg.Text("Список завдань:", font=("Arial", 12, "bold"))],
    [sg.Listbox(
        values=[],
        size=(75, 15),
        key="-TASKS-",
        enable_events=True,
        expand_x=True,
        expand_y=True
    )],
    [
        sg.Button("Редагувати", key="-EDIT-"),
        sg.Button("Видалити", key="-DELETE-"),
        sg.Button("Виконано", key="-COMPLETE-"),
        sg.Button("Оновити", key="-REFRESH-")
    ],
    [sg.Button("Вийти", key="-EXIT-")]
]
window = sg.Window(
    "TaskHub — Менеджер завдань",
    layout,
    size=(750, 550),
    resizable=True
)
refresh(window)
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "-EXIT-"):
        break
    elif event == "-ADD-":
        add_task(window, values)
    elif event == "-DELETE-":
        delete_task(window)
    elif event == "-COMPLETE-":
        complete_task(window)
    elif event == "-EDIT-":
        edit_task(window)
    elif event == "-REFRESH-":
        refresh(window)
window.close()