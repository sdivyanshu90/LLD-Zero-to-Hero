# Custom Thread Pool Executor

## Problem Summary

Design a custom thread pool executor with manual worker lifecycle management and configurable rejection policies.

## Why This Problem Is Asked

Building a thread pool from scratch validates deep understanding of producer–consumer queues, graceful shutdown, and backpressure. `concurrent.futures.ThreadPoolExecutor` is the production answer, but implementing one manually shows a candidate understands what happens under the hood: a bounded work queue, blocking workers, and the difference between `shutdown(wait=True)` and abruptly killing threads.

The rejection policy hook is the design extensibility test: when the queue is full, should the caller be blocked, should the task be dropped, or should the caller’s thread run the task itself? The choice must be pluggable rather than hardcoded.

## Functional Requirements

1. Accept submitted callables with a configurable work-queue capacity.
2. Dispatch submitted work across a fixed pool of worker threads.
3. Apply a rejection policy when the queue is full: `ABORT`, `DISCARD`, or `CALLER_RUNS`.
4. Support orderly shutdown that drains the queue before stopping workers.
5. Reject new submissions after shutdown is initiated.

## ASCII UML

```text
+-------------------+
| RejectionPolicy   |
+-------------------+
| ABORT             |
| DISCARD           |
| CALLER_RUNS       |
+-------------------+

+-------------------+
| ThreadPool        |
+-------------------+
| workers           |
| queue             |
| queue_capacity    |
+-------------------+
| submit()          |
| shutdown()        |
+-------------------+
```

## Concurrency Checklist

- Shared state: work queue and worker stop state.
- Deadlock risk: never run queued tasks while holding the queue condition lock.
- Lock granularity: one queue condition is sufficient here.
- Lock-free alternative: MPSC queues are a production-grade option beyond pure Python stdlib.

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `WorkerThread` runs tasks from the queue. `ThreadPoolExecutor` manages the pool lifecycle and submission. `RejectionPolicy` handles overflow. |
| **OCP**   | Adding a `CallerRunsPolicy` rejection strategy means one new class; the executor is unchanged.                                                |
| **LSP**   | All rejection policies satisfy the same `reject(task)` contract; the executor never branches on which policy is active.                       |
| **ISP**   | `RejectionPolicy` declares only `reject(task)`. Workers do not need to know about the rejection logic.                                        |
| **DIP**   | `ThreadPoolExecutor` holds a `RejectionPolicy` abstraction; the specific policy is injected at construction.                                  |

## Key Edge Cases

- `CALLER_RUNS` policy must execute the task in the calling thread, not silently discard it.
- Submitting work to a shut-down pool must be rejected immediately.
- A worker must release the queue lock before executing a callback.

## Follow-up Questions

1. How would you add priority levels so high-priority tasks jump the queue?
2. How would you expose metrics such as queue depth and average worker utilisation?
3. How would you implement work-stealing so idle workers take tasks from busy workers?
