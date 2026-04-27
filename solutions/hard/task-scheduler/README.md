# Task Scheduler Solution

This implementation builds a custom delay queue and a custom thread pool from conditions, deques, and heaps. Sequence numbers preserve fairness for tasks with the same due time.

## Design Notes

- `ScheduledTask` is an `order=True` dataclass comparing by `(run_at, sequence)` for heap ordering.
- `DelayQueue` wraps a min-heap with a `Condition`; `get_due()` sleeps until the next task's due time arrives.
- `WorkQueue` is a `deque` with a `Condition`; workers block until an item appears.
- `SimpleThreadPool` owns N daemon worker threads that drain `WorkQueue`.
- `TaskScheduler` runs a dispatcher thread that transfers due tasks from `DelayQueue` to `WorkQueue`.

## Complexity Analysis

| Operation                   | Time                                    | Space                                            |
| --------------------------- | --------------------------------------- | ------------------------------------------------ |
| `schedule(task)`            | O(log n), n = pending tasks (heap push) | O(1)                                             |
| `DelayQueue.get_due()`      | O(log n) heap pop when task becomes due | O(1)                                             |
| `WorkQueue.put()` / `get()` | O(1) deque ops                          | O(1)                                             |
| Worker task execution       | O(task’s own complexity)                | O(1) overhead                                    |
| Space (total)               | —                                       | O(n) delay heap + O(w) work queue + O(t) workers |

## SOLID Compliance

| Principle | Evidence                                                                                                                                                            |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `ScheduledTask` is data-only. `DelayQueue` owns time-ordered blocking retrieval. `WorkQueue` owns ready-task buffering. `TaskScheduler` owns the dispatcher thread. |
| **OCP**   | Recurring tasks need only a `recur_after_ms` field on `ScheduledTask`; the dispatcher re-enqueues after execution without changing any queue class.                 |
| **LSP**   | Any callable passed as `task.action` must be invokable with no arguments; the worker calls `action()` uniformly.                                                    |
| **ISP**   | `DelayQueue` exposes `put()` and `get_due()`. `WorkQueue` exposes `put()` and `get()`. Neither class knows about the other.                                         |
| **DIP**   | `TaskScheduler` depends on `DelayQueue` and `WorkQueue` interfaces; a database-backed delay queue is a constructor-level swap.                                      |

## Design Pattern

Two-queue pipeline: the delay queue decouples time-based scheduling from execution throughput. The dispatcher is the only thread that reads from the delay queue and writes to the work queue, so the queues never need a shared lock. Workers consume only from the work queue, keeping lock contention minimal.

## Folder Layout

```text
task-scheduler/
|-- app.py
|-- models/
|   `-- core.py      # ScheduledTask
`-- services/
    `-- scheduler.py # DelayQueue, WorkQueue, SimpleThreadPool, TaskScheduler
```

## Trade-offs

- `get_due()` wakes on a `Condition.wait(timeout=delay)`, which may fire slightly late due to OS scheduling; acceptable for educational use.
- The dispatcher is a single thread; for extreme throughput, shard the delay queue by hash of task ID across multiple dispatchers.
- No task cancellation; add a `cancelled_ids: set` and skip cancelled tasks in the dispatcher loop.

## Run

From this directory:

```bash
python3 app.py
```
