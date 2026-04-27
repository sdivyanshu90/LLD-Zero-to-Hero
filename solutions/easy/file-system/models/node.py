from __future__ import annotations

from abc import ABC, abstractmethod


class FileSystemNode(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def total_size(self) -> int:
        raise NotImplementedError