from __future__ import annotations

from datetime import datetime

from models.log_level import LogLevel
from models.log_record import LogRecord
from services.handlers import DebugHandler, ErrorHandler, InfoHandler, LogHandler, MemoryHandler


class Logger:
    _instance: "Logger | None" = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        info_handler = InfoHandler()
        debug_handler = DebugHandler()
        error_handler = ErrorHandler()
        info_handler.set_next(debug_handler).set_next(error_handler)

        self._chain: LogHandler = info_handler
        self._handlers: dict[LogLevel, MemoryHandler] = {
            LogLevel.INFO: info_handler,
            LogLevel.DEBUG: debug_handler,
            LogLevel.ERROR: error_handler,
        }
        self._initialized = True

    def log(self, level: LogLevel, message: str) -> str:
        record = LogRecord(level=level, message=message, created_at=datetime.now())
        handled = self._chain.handle(record)
        if not handled:
            raise ValueError(f"Unsupported log level: {level}")
        return record.render()

    def history_for(self, level: LogLevel) -> list[str]:
        return list(self._handlers[level].messages)