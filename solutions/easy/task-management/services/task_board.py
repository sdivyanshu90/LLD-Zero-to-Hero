from __future__ import annotations

from dataclasses import dataclass, field

from models.task_component import TaskComponent


@dataclass(slots=True)
class TaskBoard:
    root_tasks: list[TaskComponent] = field(default_factory=list)

    def add_root_task(self, task: TaskComponent) -> None:
        self.root_tasks.append(task)

    def overall_completion(self) -> float:
        if not self.root_tasks:
            return 0.0
        total = sum(task.completion_percentage() for task in self.root_tasks)
        return total / len(self.root_tasks)

    def snapshot(self) -> list[str]:
        lines: list[str] = []
        for task in self.root_tasks:
            lines.extend(task.render())
        return lines