from dataclasses import dataclass, field
from typing import Callable


@dataclass(order=True, slots=True)
class ScheduledTask:
    run_at: float
    sequence: int
    task_id: str = field(compare=False)
    callback: Callable[..., None] = field(compare=False)
    args: tuple[object, ...] = field(default_factory=tuple, compare=False)

    def run(self) -> None:
        self.callback(*self.args)