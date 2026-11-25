import argparse
import sys
import click
import typer
from typer.main import get_command
from tasks import (
    add_task,
    show_tasks,
    edit_task,
    delete_task,
    complete_task,
    show_stats,
    clear_tasks
)
typer_app = typer.Typer()
@click.group()
def click_app():
    pass
@click_app.command()
@click.argument("text")
@click.option("--deadline", default=None, help="Дата у форматі ДД.ММ.РРРР")
def add(text, deadline):
    try:
        add_task(text, deadline)
    except ValueError as error:
        raise click.ClickException(str(error))
@click_app.command()
def show():
    show_tasks()
@click_app.command()
@click.argument("task_id", type=int)
def delete(task_id):
    try:
        delete_task(task_id)
    except ValueError as error:
        raise click.ClickException(str(error))
@typer_app.command()
def stats():
    show_stats()
@typer_app.command()
def overdue():
    from storage import load_Hello
    from deadlines import is_overdue
    Hello = load_Hello()
    tasks = [task for task in Hello if is_overdue(task)]
    if not tasks:
        typer.echo("Прострочених завдань немає.")
        return
    typer.echo("Прострочені завдання:")
    for task in tasks:
        typer.echo(f'[{task["id"]}] {task["text"]} | Дедлайн: {task["deadline"]}')
@typer_app.command()
def clear(
    yes: bool = typer.Option(False, "--yes", help="Підтвердити видалення без запитання")
):
    if yes or typer.confirm("Ви дійсно хочете видалити всі завдання?"):
        clear_tasks()
    else:
        typer.echo("Операцію скасовано.")
def argparse_main(arguments):
    parser = argparse.ArgumentParser(
        description="TaskHub — консольний менеджер завдань"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_parser = subparsers.add_parser("add", help="Додати завдання")
    add_parser.add_argument("text", help="Назва завдання")
    add_parser.add_argument("--deadline", help="Дата ДД.ММ.РРРР")
    subparsers.add_parser("show", help="Показати завдання")
    edit_parser = subparsers.add_parser("edit", help="Редагувати завдання")
    edit_parser.add_argument("id", type=int, help="Номер завдання")
    edit_parser.add_argument("--text", help="Нова назва")
    edit_parser.add_argument("--deadline", help="Новий дедлайн")
    edit_parser.add_argument("--clear-deadline", action="store_true", help="Видалити дедлайн")
    delete_parser = subparsers.add_parser("delete", help="Видалити завдання")
    delete_parser.add_argument("id", type=int)
    complete_parser = subparsers.add_parser("complete", help="Позначити як виконане")
    complete_parser.add_argument("id", type=int)
    subparsers.add_parser("stats", help="Статистика завдань")
    clear_parser = subparsers.add_parser("clear", help="Видалити всі завдання")
    clear_parser.add_argument("--yes", action="store_true")
    args = parser.parse_args(arguments)
    try:
        if args.command == "add":
            add_task(args.text, args.deadline)
        elif args.command == "show":
            show_tasks()
        elif args.command == "edit":
            if args.text is None and args.deadline is None and not args.clear_deadline:
                parser.error("Потрібно вказати --text, --deadline або --clear-deadline.")
            edit_task(
                args.id,
                args.text,
                args.deadline,
                args.clear_deadline
            )
        elif args.command == "delete":
            delete_task(args.id)
        elif args.command == "complete":
            complete_task(args.id)
        elif args.command == "stats":
            show_stats()
        elif args.command == "clear":
            if args.yes:
                clear_tasks()
            else:
                confirmation = input("Видалити всі завдання? (так/ні): ")

                if confirmation.lower() == "так":
                    clear_tasks()
                else:
                    print("Операцію скасовано.")
    except ValueError as error:
        print(f"Помилка: {error}")
        sys.exit(1)
def main():
    arguments = sys.argv[1:]
    if arguments and arguments[0] == "click":
        click_app.main(args=arguments[1:], prog_name="taskhub click")
    elif arguments and arguments[0] == "typer":
        typer_command = get_command(typer_app)
        typer_command.main(args=arguments[1:], prog_name="taskhub typer")
    else:
        argparse_main(arguments)
if __name__ == "__main__":
    main()