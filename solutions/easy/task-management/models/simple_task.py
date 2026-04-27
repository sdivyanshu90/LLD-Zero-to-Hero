from __future__ import annotations

from models.task_component import TaskComponent


class SimpleTask(TaskComponent):
    def __init__(self, title: str, completed: bool = False) -> None:
        super().__init__(title)
        self.completed = completed

    def completion_percentage(self) -> float:
        return 100.0 if self.completed else 0.0

    def mark_complete(self) -> None:
        self.completed = True

    def render(self, depth: int = 0) -> list[str]:
        status = "done" if self.completed else "todo"
        return [f"{'  ' * depth}- {self.title} [{status}]"]