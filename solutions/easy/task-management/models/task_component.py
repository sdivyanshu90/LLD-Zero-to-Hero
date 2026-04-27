from __future__ import annotations

from abc import ABC, abstractmethod


class TaskComponent(ABC):
    def __init__(self, title: str) -> None:
        self.title = title

    @abstractmethod
    def completion_percentage(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def mark_complete(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self, depth: int = 0) -> list[str]:
        raise NotImplementedError