from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from models.core import WorkItem


class RejectionPolicy(Enum):
    ABORT = "abort"
    DISCARD = "discard"
    CALLER_RUNS = "caller_runs"


@dataclass(slots=True)
class ThreadPoolExecutor:
    worker_count: int
    queue_capacity: int
    rejection_policy: RejectionPolicy
    _queue: deque[WorkItem] = field(default_factory=deque, init=False, repr=False)
    _condition: threading.Condition = field(default_factory=threading.Condition, init=False, repr=False)
    _stop_event: threading.Event = field(default_factory=threading.Event, init=False, repr=False)
    _workers: list[threading.Thread] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        for index in range(self.worker_count):
            worker = threading.Thread(target=self._worker_loop, name=f"pool-worker-{index}", daemon=True)
            worker.start()
            self._workers.append(worker)

    def submit(self, callback: Callable[..., None], *args: object) -> None:
        work_item = WorkItem(callback=callback, args=args)
        with self._condition:
            if len(self._queue) >= self.queue_capacity:
                self._reject(work_item)
                return
            self._queue.append(work_item)
            self._condition.notify()

    def shutdown(self) -> None:
        self._stop_event.set()
        with self._condition:
            self._condition.notify_all()
        for worker in self._workers:
            worker.join(timeout=1)

    def _worker_loop(self) -> None:
        while not self._stop_event.is_set():
            with self._condition:
                while not self._queue and not self._stop_event.is_set():
                    self._condition.wait(timeout=0.1)
                if not self._queue:
                    continue
                work_item = self._queue.popleft()
            work_item.run()

    def _reject(self, work_item: WorkItem) -> None:
        if self.rejection_policy is RejectionPolicy.ABORT:
            raise ValueError("Task queue is full")
        if self.rejection_policy is RejectionPolicy.DISCARD:
            return
        if self.rejection_policy is RejectionPolicy.CALLER_RUNS:
            work_item.run()