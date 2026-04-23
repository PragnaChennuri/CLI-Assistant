from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from .models import Task, utc_now_iso
from .storage import JsonTaskStorage


class TaskManager:
    def __init__(self, storage: JsonTaskStorage) -> None:
        self.storage = storage
        self._next_id, self._tasks = self.storage.load()

    def _persist(self) -> None:
        self.storage.save(self._next_id, self._tasks)

    def _find(self, task_id: int) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task {task_id} not found")

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str | None = None,
        due_date: str | None = None,
    ) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty")

        task = Task(
            id=self._next_id,
            title=title,
            description=description.strip(),
            priority=priority,
            due_date=due_date,
        )
        self._tasks.append(task)
        self._next_id += 1
        self._persist()
        return task

    def list_tasks(self, include_completed: bool = True, status: str | None = None) -> list[Task]:
        tasks: Iterable[Task] = self._tasks
        if status == "pending":
            tasks = [t for t in tasks if not t.completed]
        elif status == "completed":
            tasks = [t for t in tasks if t.completed]
        elif not include_completed:
            tasks = [t for t in tasks if not t.completed]
        return list(tasks)

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        due_date: str | None = None,
    ) -> Task:
        task = self._find(task_id)

        new_task = replace(
            task,
            title=task.title if title is None else title.strip(),
            description=task.description if description is None else description.strip(),
            priority=task.priority if priority is None else priority,
            due_date=task.due_date if due_date is None else due_date,
        )
        if not new_task.title:
            raise ValueError("Title cannot be empty")

        index = self._tasks.index(task)
        self._tasks[index] = new_task
        self._persist()
        return new_task

    def complete_task(self, task_id: int) -> Task:
        task = self._find(task_id)
        if task.completed:
            return task
        index = self._tasks.index(task)
        updated = replace(task, completed=True, completed_at=utc_now_iso())
        self._tasks[index] = updated
        self._persist()
        return updated

    def delete_task(self, task_id: int) -> None:
        task = self._find(task_id)
        self._tasks.remove(task)
        self._persist()

    def stats(self) -> dict[str, int]:
        total = len(self._tasks)
        completed = len([t for t in self._tasks if t.completed])
        pending = total - completed
        return {"total": total, "completed": completed, "pending": pending}
