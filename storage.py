import json
from pathlib import Path
FILE_NAME = Path(__file__).with_name("Hello.json")
def load_Hello():
    if not FILE_NAME.exists():
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Файл Hello.json містить некоректні дані.")
    if isinstance(data, dict):
        data = data.get("tasks", [])
    if not isinstance(data, list):
        raise ValueError("Неправильний формат файлу Hello.json.")
    Hello = []
    for index, item in enumerate(data, start=1):
        if isinstance(item, str):
            item = {
                "id": index,
                "text": item,
                "deadline": None,
                "completed": False
            }
        if not isinstance(item, dict):
            continue
        Hello.append({
            "id": item.get("id", index),
            "text": str(item.get("text", "")),
            "deadline": item.get("deadline"),
            "completed": bool(item.get("completed", False))
        })
    return Hello
def save_Hello(Hello):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(Hello, file, ensure_ascii=False, indent=4)