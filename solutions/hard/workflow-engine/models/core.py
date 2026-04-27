from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True, slots=True)
class WorkflowTask:
    task_id: str
    dependencies: set[str]
    action: Callable[[], None]