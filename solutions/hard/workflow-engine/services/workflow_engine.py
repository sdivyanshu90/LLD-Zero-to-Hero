from __future__ import annotations

import threading
from dataclasses import dataclass, field

from models.core import WorkflowTask


@dataclass(slots=True)
class WorkflowEngine:
    tasks: list[WorkflowTask]
    _task_map: dict[str, WorkflowTask] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._task_map = {task.task_id: task for task in self.tasks}

    def execute(self) -> list[list[str]]:
        indegree = {task.task_id: len(task.dependencies) for task in self.tasks}
        dependents: dict[str, list[str]] = {task.task_id: [] for task in self.tasks}
        for task in self.tasks:
            for dependency in task.dependencies:
                dependents.setdefault(dependency, []).append(task.task_id)

        waves: list[list[str]] = []
        ready = sorted(task_id for task_id, count in indegree.items() if count == 0)
        completed_count = 0

        while ready:
            current_wave = ready
            ready = []
            waves.append(current_wave)
            threads: list[threading.Thread] = []

            for task_id in current_wave:
                task = self._task_map[task_id]
                thread = threading.Thread(target=task.action)
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            completed_count += len(current_wave)
            for task_id in current_wave:
                for dependent_id in dependents.get(task_id, []):
                    indegree[dependent_id] -= 1
                    if indegree[dependent_id] == 0:
                        ready.append(dependent_id)
            ready.sort()

        if completed_count != len(self.tasks):
            raise ValueError("Workflow contains a cycle")

        return waves