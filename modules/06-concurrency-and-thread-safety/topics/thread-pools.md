# Thread Pools

> **The one-line idea:** Pre-create a fixed number of worker threads and reuse them for many tasks — eliminating the overhead of creating and destroying a thread per task.

---

## Real-World Analogy — Restaurant Kitchen

```
WITHOUT a thread pool:
  Every time a customer orders, you hire a new chef,
  they cook the meal, then you fire them.
  Hiring/firing overhead dwarfs the cooking time for short orders.

WITH a thread pool:
  You hire 5 chefs permanently.
  Customer orders go into a queue (order tickets).
  An idle chef picks up the next ticket.
  After finishing, the chef is immediately available for the next ticket.
  No hiring/firing overhead. Workload scales up to 5 concurrent orders.
```

---

## Thread Pool Architecture

```
                         ┌──────────────────────────────────────┐
  submit(task_1) ──────► │           TASK QUEUE                 │
  submit(task_2) ──────► │  [ task_4 | task_3 | task_2 | task_1]│
  submit(task_3) ──────► │          (FIFO — oldest first)       │
  submit(task_4) ──────► └──────────────────────────────────────┘
                                           │
                     ┌─────────────────────┼──────────────────────┐
                     │                     │                      │
                     ▼                     ▼                      ▼
             ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
             │  Worker 1   │      │  Worker 2   │      │  Worker 3   │
             │ [task_1]    │      │ [task_2]    │      │  (idle)     │
             │  running    │      │  running    │      │  waiting    │
             └─────────────┘      └─────────────┘      └─────────────┘

  When Worker 1 finishes task_1:
    → picks up task_3 from the queue
    → begins executing it
```

---

## New Thread Per Task vs. Thread Pool

```
┌──────────────────────┬────────────────────────────┬──────────────────────────┐
│ DIMENSION            │ NEW THREAD PER TASK         │ THREAD POOL              │
├──────────────────────┼────────────────────────────┼──────────────────────────┤
│ Thread creation cost │ Paid every task             │ Paid once at startup     │
│ Memory usage         │ Unbounded (1 thread / task) │ Bounded (fixed pool size)│
│ Max concurrency      │ Uncontrolled — can crash OS │ Controlled by pool size  │
│ Startup latency      │ High per task               │ Low (thread already ready│
│ Complex task mgmt    │ Manual                      │ Handled by executor      │
│ Best for             │ Rare, long-lived tasks      │ Many short-lived tasks   │
└──────────────────────┴────────────────────────────┴──────────────────────────┘
```

---

## Pool Sizing Guidance

```
I/O-BOUND TASKS (network calls, file reads, DB queries):
  Threads spend most of their time WAITING (GIL released).
  More threads → more concurrent I/O in flight.
  Rule of thumb: pool_size = 2 × num_CPU_cores  (or more, experiment)

CPU-BOUND TASKS (heavy computation):
  Threads spend time on Python bytecode (GIL limits concurrency).
  Rule of thumb: pool_size = num_CPU_cores
  Better tool: multiprocessing.ProcessPoolExecutor (bypasses GIL)
```

---

## Future / Promise — Getting Results Back

```
A Future represents the eventual result of a task:

  with ThreadPoolExecutor(max_workers=4) as executor:
      future_a = executor.submit(fetch_url, "https://api.example.com/a")
      future_b = executor.submit(fetch_url, "https://api.example.com/b")
      future_c = executor.submit(fetch_url, "https://api.example.com/c")

      # All three fetches run concurrently.
      # Collect results when ready:
      result_a = future_a.result()   # blocks until task_a done
      result_b = future_b.result()   # likely already done by now
      result_c = future_c.result()

  Futures allow:
    - Checking if done: future.done()
    - Cancelling if not started: future.cancel()
    - Adding a callback: future.add_done_callback(fn)
    - Waiting for many at once: concurrent.futures.wait([f1, f2, f3])
    - Iterating as completed: concurrent.futures.as_completed([f1, f2])
```

---

## Executor Hierarchy

```
concurrent.futures
         │
         ├── Executor (abstract base)
         │       + submit(fn, *args) → Future
         │       + map(fn, *iterables) → iterator
         │       + shutdown(wait=True)
         │
         ├── ThreadPoolExecutor
         │       Uses threads — good for I/O-bound work
         │       Bound by GIL for CPU-bound work
         │
         └── ProcessPoolExecutor
                 Uses separate processes — bypasses GIL
                 Good for CPU-bound work
                 Higher overhead (inter-process communication)
```

---

## Thread Pool Checklist

```
  □  Did you use `with ThreadPoolExecutor(...) as executor:` to ensure
     clean shutdown? (context manager calls shutdown() automatically)

  □  Did you choose pool size based on whether tasks are I/O-bound
     or CPU-bound?

  □  Are you using ProcessPoolExecutor for CPU-heavy work?
     Threading + GIL won't help for CPU-bound tasks in CPython.

  □  Are task functions pure / stateless where possible?
     Shared mutable state between tasks reintroduces race conditions.

  □  Are you collecting Future.result() and handling exceptions?
     Unhandled exceptions inside tasks are silently swallowed unless
     you call future.result() which re-raises them.
```
