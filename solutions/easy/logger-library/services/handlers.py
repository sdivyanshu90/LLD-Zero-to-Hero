from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from models.log_level import LogLevel
from models.log_record import LogRecord


class LogHandler(ABC):
    def __init__(self) -> None:
        self._next_handler: Optional[LogHandler] = None

    def set_next(self, handler: "LogHandler") -> "LogHandler":
        self._next_handler = handler
        return handler

    def handle(self, record: LogRecord) -> bool:
        if self.can_handle(record.level):
            self.write(record)
            return True

        if self._next_handler is None:
            return False

        return self._next_handler.handle(record)

    @abstractmethod
    def can_handle(self, level: LogLevel) -> bool:
        raise NotImplementedError

    @abstractmethod
    def write(self, record: LogRecord) -> None:
        raise NotImplementedError


class MemoryHandler(LogHandler):
    def __init__(self, level: LogLevel) -> None:
        super().__init__()
        self.level = level
        self.messages: list[str] = []

    def can_handle(self, level: LogLevel) -> bool:
        return level is self.level

    def write(self, record: LogRecord) -> None:
        self.messages.append(record.render())


class InfoHandler(MemoryHandler):
    def __init__(self) -> None:
        super().__init__(LogLevel.INFO)


class DebugHandler(MemoryHandler):
    def __init__(self) -> None:
        super().__init__(LogLevel.DEBUG)


class ErrorHandler(MemoryHandler):
    def __init__(self) -> None:
        super().__init__(LogLevel.ERROR)