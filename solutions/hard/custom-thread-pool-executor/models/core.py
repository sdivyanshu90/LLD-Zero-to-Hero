from dataclasses import dataclass, field
from typing import Callable


@dataclass(slots=True)
class WorkItem:
    callback: Callable[..., None]
    args: tuple[object, ...] = field(default_factory=tuple)

    def run(self) -> None:
        self.callback(*self.args)