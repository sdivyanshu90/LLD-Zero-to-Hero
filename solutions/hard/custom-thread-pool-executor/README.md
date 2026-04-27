# Custom Thread Pool Executor Solution

This implementation manages workers and a bounded queue directly, with configurable rejection behavior when the queue is full.

## Design Notes

- `WorkItem` wraps a callable and its arguments.
- `RejectionPolicy` is an `Enum` with `ABORT`, `DISCARD`, and `CALLER_RUNS` variants.
- `ThreadPool` owns the bounded `deque`, a `Condition` for worker coordination, and a list of daemon worker threads.
- Workers block on the condition until an item is available or shutdown is signalled.

## Complexity Analysis

| Operation             | Time                   | Space                                  |
| --------------------- | ---------------------- | -------------------------------------- |
| `submit(task)`        | O(1) deque append      | O(1)                                   |
| Worker `_run()` loop  | O(1) per task dequeue  | O(1)                                   |
| `shutdown(wait=True)` | O(w), w = worker count | O(1)                                   |
| Space (total)         | —                      | O(q) for work queue + O(w) for workers |

## SOLID Compliance

| Principle | Evidence                                                                                                                                                      |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `WorkItem` is a pure task wrapper. `ThreadPool` manages the queue, workers, and shutdown lifecycle. Rejection logic is isolated in the policy variant.        |
| **OCP**   | Adding a new rejection policy (e.g., `WAIT_AND_RETRY`) means a new policy value and one new branch in `_apply_rejection()`; the core pool logic is unchanged. |
| **LSP**   | All rejection policies produce a defined outcome (raise, discard, or run inline) when `submit()` finds the queue full.                                        |
| **ISP**   | `ThreadPool` exposes only `submit()`, `shutdown()`, and `size()`. Workers never call pool methods from inside `_run()`.                                       |
| **DIP**   | `ThreadPool` calls `work_item.run()` through the `WorkItem` interface; it does not know the callable type.                                                    |

## Design Pattern

Producer–consumer with bounded queue: `submit()` is the producer; worker threads are consumers. A single `Condition` coordinates both sides. The rejection policy is applied at submit time if the queue is at capacity, avoiding any lock held during callback execution.

## Folder Layout

```text
custom-thread-pool-executor/
|-- app.py
|-- models/
|   `-- core.py      # WorkItem, RejectionPolicy
`-- services/
    `-- thread_pool.py # ThreadPool
```

## Trade-offs

- `CALLER_RUNS` executes the task synchronously in the submitter's thread, which can create back-pressure naturally without discarding work.
- Workers are daemon threads so the process exits cleanly even if `shutdown()` is not called; production code should call `shutdown()` explicitly.
- Queue capacity is per-pool; a priority queue variant would require a different underlying structure.

## Run

From this directory:

```bash
python3 app.py
```
