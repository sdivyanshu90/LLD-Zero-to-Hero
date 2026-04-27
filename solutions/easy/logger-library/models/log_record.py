from dataclasses import dataclass
from datetime import datetime

from .log_level import LogLevel


@dataclass(frozen=True, slots=True)
class LogRecord:
    level: LogLevel
    message: str
    created_at: datetime

    def render(self) -> str:
        timestamp = self.created_at.isoformat(timespec="seconds")
        return f"[{timestamp}] {self.level.value}: {self.message}"