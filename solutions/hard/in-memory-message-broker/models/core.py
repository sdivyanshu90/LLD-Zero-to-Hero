from __future__ import annotations

import threading
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Message:
    offset: int
    payload: str


@dataclass(slots=True)
class TopicLog:
    messages: list[Message] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def append(self, payload: str) -> int:
        with self.lock:
            offset = len(self.messages)
            self.messages.append(Message(offset=offset, payload=payload))
            return offset

    def read_from(self, offset: int, batch_size: int) -> list[Message]:
        with self.lock:
            return list(self.messages[offset : offset + batch_size])