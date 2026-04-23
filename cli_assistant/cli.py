from __future__ import annotations

import argparse
from typing import Sequence

from .manager import TaskManager
from .storage import JsonTaskStorage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI task management assistant")
    parser.add_argument("--storage", default="tasks.json", help="Path to task storage file")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title")
    add_parser.add_argument("--description", default="")
    add_parser.add_argument("--priority")
    add_parser.add_argument("--due-date")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--all", action="store_true", help="Include completed tasks")
    list_parser.add_argument("--status", choices=["pending", "completed"])

    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("id", type=int)
    update_parser.add_argument("--title")
    update_parser.add_argument("--description")
    update_parser.add_argument("--priority")
    update_parser.add_argument("--due-date")

    complete_parser = subparsers.add_parser("complete", help="Mark a task complete")
    complete_parser.add_argument("id", type=int)

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int)

    subparsers.add_parser("stats", help="Show productivity statistics")

    return parser


def format_task_line(task) -> str:
    status = "done" if task.completed else "todo"
    parts = [f"[{task.id}]", status, task.title]
    if task.priority:
        parts.append(f"priority={task.priority}")
    if task.due_date:
        parts.append(f"due={task.due_date}")
    return " | ".join(parts)


def run(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    manager = TaskManager(JsonTaskStorage(args.storage))

    try:
        if args.command == "add":
            task = manager.add_task(
                title=args.title,
                description=args.description,
                priority=args.priority,
                due_date=args.due_date,
            )
            print(f"Created task {task.id}: {task.title}")
            return 0

        if args.command == "list":
            tasks = manager.list_tasks(include_completed=args.all, status=args.status)
            if not tasks:
                print("No tasks found")
                return 0
            for task in tasks:
                print(format_task_line(task))
            return 0

        if args.command == "update":
            task = manager.update_task(
                task_id=args.id,
                title=args.title,
                description=args.description,
                priority=args.priority,
                due_date=args.due_date,
            )
            print(f"Updated task {task.id}")
            return 0

        if args.command == "complete":
            task = manager.complete_task(args.id)
            print(f"Completed task {task.id}")
            return 0

        if args.command == "delete":
            manager.delete_task(args.id)
            print(f"Deleted task {args.id}")
            return 0

        if args.command == "stats":
            stats = manager.stats()
            print(f"Total: {stats['total']}")
            print(f"Completed: {stats['completed']}")
            print(f"Pending: {stats['pending']}")
            return 0
    except ValueError as exc:
        print(f"Error: {exc}")
        return 1

    parser.print_help()
    return 1
