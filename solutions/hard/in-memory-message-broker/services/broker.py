from __future__ import annotations

import threading
from dataclasses import dataclass, field

from models.core import Message, TopicLog


@dataclass(slots=True)
class MessageBroker:
    topics: dict[str, TopicLog] = field(default_factory=dict)
    committed_offsets: dict[tuple[str, str], int] = field(default_factory=dict)
    _offset_lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def create_topic(self, topic: str) -> None:
        self.topics.setdefault(topic, TopicLog())

    def publish(self, topic: str, payload: str) -> int:
        return self._get_topic(topic).append(payload)

    def poll(self, topic: str, consumer_id: str, batch_size: int) -> list[Message]:
        with self._offset_lock:
            offset = self.committed_offsets.get((topic, consumer_id), 0)
        return self._get_topic(topic).read_from(offset, batch_size)

    def ack(self, topic: str, consumer_id: str, last_processed_offset: int) -> None:
        with self._offset_lock:
            current = self.committed_offsets.get((topic, consumer_id), 0)
            self.committed_offsets[(topic, consumer_id)] = max(current, last_processed_offset + 1)

    def _get_topic(self, topic: str) -> TopicLog:
        topic_log = self.topics.get(topic)
        if topic_log is None:
            raise ValueError(f"Unknown topic {topic}")
        return topic_log