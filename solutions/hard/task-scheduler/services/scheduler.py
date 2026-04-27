from __future__ import annotations

import heapq
import itertools
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Callable

from models.core import ScheduledTask


@dataclass(slots=True)
class DelayQueue:
    _heap: list[ScheduledTask] = field(default_factory=list, init=False)
    _condition: threading.Condition = field(default_factory=threading.Condition, init=False, repr=False)

    def put(self, task: ScheduledTask) -> None:
        with self._condition:
            heapq.heappush(self._heap, task)
            self._condition.notify_all()

    def get_due(self, stop_event: threading.Event) -> ScheduledTask | None:
        with self._condition:
            while not stop_event.is_set():
                if not self._heap:
                    self._condition.wait(timeout=0.1)
                    continue
                next_task = self._heap[0]
                delay = next_task.run_at - time.monotonic()
                if delay <= 0:
                    return heapq.heappop(self._heap)
                self._condition.wait(timeout=delay)
            return None


@dataclass(slots=True)
class WorkQueue:
    _tasks: deque[ScheduledTask] = field(default_factory=deque, init=False)
    _condition: threading.Condition = field(default_factory=threading.Condition, init=False, repr=False)

    def put(self, task: ScheduledTask) -> None:
        with self._condition:
            self._tasks.append(task)
            self._condition.notify()

    def get(self, stop_event: threading.Event) -> ScheduledTask | None:
        with self._condition:
            while not self._tasks and not stop_event.is_set():
                self._condition.wait(timeout=0.1)
            if self._tasks:
                return self._tasks.popleft()
            return None


@dataclass(slots=True)
class SimpleThreadPool:
    worker_count: int
    _stop_event: threading.Event = field(default_factory=threading.Event, init=False, repr=False)
    _queue: WorkQueue = field(default_factory=WorkQueue, init=False, repr=False)
    _workers: list[threading.Thread] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        for index in range(self.worker_count):
            worker = threading.Thread(target=self._worker_loop, name=f"worker-{index}", daemon=True)
            worker.start()
            self._workers.append(worker)

    def submit(self, task: ScheduledTask) -> None:
        self._queue.put(task)

    def shutdown(self) -> None:
        self._stop_event.set()
        for worker in self._workers:
            worker.join(timeout=1)

    def _worker_loop(self) -> None:
        while not self._stop_event.is_set():
            task = self._queue.get(self._stop_event)
            if task is None:
                continue
            task.run()


@dataclass(slots=True)
class TaskScheduler:
    worker_count: int
    _delay_queue: DelayQueue = field(default_factory=DelayQueue, init=False, repr=False)
    _thread_pool: SimpleThreadPool = field(init=False, repr=False)
    _stop_event: threading.Event = field(default_factory=threading.Event, init=False, repr=False)
    _counter: itertools.count = field(default_factory=itertools.count, init=False, repr=False)
    _dispatcher: threading.Thread = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._thread_pool = SimpleThreadPool(worker_count=self.worker_count)
        self._dispatcher = threading.Thread(target=self._dispatch_loop, daemon=True)
        self._dispatcher.start()

    def schedule(self, task_id: str, delay_seconds: float, callback: Callable[..., None], *args: object) -> None:
        scheduled_task = ScheduledTask(
            run_at=time.monotonic() + delay_seconds,
            sequence=next(self._counter),
            task_id=task_id,
            callback=callback,
            args=args,
        )
        self._delay_queue.put(scheduled_task)

    def shutdown(self) -> None:
        self._stop_event.set()
        self._dispatcher.join(timeout=1)
        self._thread_pool.shutdown()

    def _dispatch_loop(self) -> None:
        while not self._stop_event.is_set():
            task = self._delay_queue.get_due(self._stop_event)
            if task is None:
                continue
            self._thread_pool.submit(task)