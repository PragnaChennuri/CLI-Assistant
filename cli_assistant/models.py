from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: str | None = None
    due_date: str | None = None
    created_at: str = ""
    completed_at: str | None = None

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = utc_now_iso()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(**data)
