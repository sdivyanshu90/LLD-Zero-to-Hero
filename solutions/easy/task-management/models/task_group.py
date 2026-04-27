from __future__ import annotations

from models.task_component import TaskComponent


class TaskGroup(TaskComponent):
    def __init__(self, title: str) -> None:
        super().__init__(title)
        self.children: list[TaskComponent] = []

    def add(self, task: TaskComponent) -> None:
        self.children.append(task)

    def completion_percentage(self) -> float:
        if not self.children:
            return 0.0
        total = sum(child.completion_percentage() for child in self.children)
        return total / len(self.children)

    def mark_complete(self) -> None:
        for child in self.children:
            child.mark_complete()

    def render(self, depth: int = 0) -> list[str]:
        lines = [f"{'  ' * depth}+ {self.title} ({self.completion_percentage():.1f}%)"]
        for child in self.children:
            lines.extend(child.render(depth + 1))
        return lines