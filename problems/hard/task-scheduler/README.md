# Task Scheduler

## Problem Summary

Design a task scheduler with a custom delay queue and a custom thread pool that dispatches due work without starving ready tasks.

## Why This Problem Is Asked

`java.util.concurrent.ScheduledThreadPoolExecutor` and Python’s `sched` module both implement variants of this two-queue pipeline. Building it from scratch tests whether a candidate understands why two queues are needed: the delay queue decouples time-tracking from execution, and the work queue decouples dispatch from execution throughput.

The correct dispatcher uses a `Condition.wait(timeout=delay_until_next)` so that it wakes precisely when the next task is due — not on a fixed polling interval that could stall work.

## Functional Requirements

1. Schedule tasks for future execution.
2. Hold pending work in a delay queue.
3. Dispatch due tasks into a worker pool.
4. Preserve fair execution order for tasks with equal due time.
5. Shut down cleanly.

## ASCII UML

```text
+-------------------+
| ScheduledTask     |
+-------------------+
| run_at            |
| sequence          |
| callback          |
+-------------------+

+-------------------+
| DelayQueue        |
+-------------------+
| heap              |
| condition         |
+-------------------+
| put()             |
| get_due()         |
+-------------------+

+-------------------+
| ThreadPool        |
+-------------------+
| workers           |
| work_queue        |
+-------------------+
| submit()          |
| shutdown()        |
+-------------------+
```

## Concurrency Checklist

- Shared state: heap and worker queue need condition-protected access.
- Deadlock risk: do not hold the delay-queue lock while executing callbacks.
- Lock granularity: separate delay-queue and work-queue coordination.
- Lock-free alternative: specialized runtimes use lock-free queues; Python stdlib does not expose that level directly.

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                                  |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `ScheduledTask` is a data class only. `DelayQueue` owns time-ordering and blocking get. `WorkQueue` owns the ready buffer. `TaskScheduler` owns the dispatcher. |
| **OCP**   | Recurring tasks add a `recur_after_ms` field on `ScheduledTask`; the dispatcher re-enqueues after execution without changing `DelayQueue` or `WorkQueue`.       |
| **LSP**   | Any callable passed as a task must be invokable with no arguments; the worker thread calls `task.action()` uniformly.                                           |
| **ISP**   | `DelayQueue` exposes `put()` and `get_due()`. `WorkQueue` exposes `put()` and `get()`. Neither knows about the other.                                           |
| **DIP**   | `TaskScheduler` depends on `DelayQueue` and `WorkQueue` abstractions; switching to a database-backed delay queue is a constructor-level change only.            |

## Key Edge Cases

- Tasks scheduled with the same due time must be dispatched in FIFO sequence-number order.
- Shutdown must not execute tasks that have not yet been dispatched to the work queue.
- A callback that raises an exception must not crash the worker thread.

## Follow-up Questions

1. How would you add support for recurring tasks with cron-style intervals?
2. How would you persist the delay queue so scheduled tasks survive a process restart?
3. How would you support task cancellation by task ID before the due time arrives?
