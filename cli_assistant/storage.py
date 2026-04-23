from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Task


class JsonTaskStorage:
    def __init__(self, file_path: str | Path = "tasks.json") -> None:
        self.file_path = Path(file_path)

    def load(self) -> tuple[int, list[Task]]:
        if not self.file_path.exists():
            return 1, []

        raw = json.loads(self.file_path.read_text(encoding="utf-8"))
        next_id = int(raw.get("next_id", 1))
        tasks = [Task.from_dict(item) for item in raw.get("tasks", [])]
        return next_id, tasks

    def save(self, next_id: int, tasks: list[Task]) -> None:
        payload: dict[str, Any] = {
            "next_id": next_id,
            "tasks": [task.to_dict() for task in tasks],
        }
        self.file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
