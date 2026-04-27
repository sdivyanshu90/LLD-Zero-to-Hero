# Threads and Concurrency

> **The one-line idea:** Threads let a program do multiple things at once — but sharing memory between them requires careful coordination to avoid chaos.

---

## Concurrency vs. Parallelism

```
CONCURRENCY — one CPU, interleaved execution (illusion of simultaneity):

  Time ──────────────────────────────────────────────────►
  Core 0: [████Thread A████][░░░░Thread B░░░░][████Thread A████][░░░░Thread B░░░░]

  Thread A and B take turns. Only one runs at a time.
  Useful when tasks are I/O-bound (waiting for network, disk, etc.)

PARALLELISM — multiple CPUs, truly simultaneous execution:

  Time ──────────────────────────────────────────────────►
  Core 0: [████Thread A████████████████████████████████]
  Core 1: [████Thread B████████████████████████████████]

  Thread A and B literally run at the same time.
  Useful when tasks are CPU-bound (heavy computation).
```

---

## Process vs. Thread

```
┌────────────────────────────────────────────────────────────────────┐
│                           PROCESS                                  │
│                                                                    │
│   ┌──────────────────────────────────────────────────────────┐    │
│   │                  SHARED MEMORY (Heap)                    │    │
│   │   Global variables, objects, file handles                │    │
│   └──────────────────────────────────────────────────────────┘    │
│                                                                    │
│   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐          │
│   │   Thread 1   │   │   Thread 2   │   │   Thread 3   │          │
│   │  ─────────   │   │  ─────────   │   │  ─────────   │          │
│   │  Own Stack   │   │  Own Stack   │   │  Own Stack   │          │
│   │  Own Regs    │   │  Own Regs    │   │  Own Regs    │          │
│   │  Own PC      │   │  Own PC      │   │  Own PC      │          │
│   └──────────────┘   └──────────────┘   └──────────────┘          │
└────────────────────────────────────────────────────────────────────┘

Threads SHARE the heap but each has its OWN stack, registers, and
program counter (instruction pointer).

Creating a new process = expensive (new memory space, OS resources)
Creating a new thread  = cheap (shared memory space, lightweight)
```

---

## Thread Lifecycle — State Machine

```
                       ┌─────────────────────┐
    Thread created ──► │       NEW            │
                       └─────────────────────┘
                                 │
                        start()  │
                                 ▼
                       ┌─────────────────────┐
                       │     RUNNABLE         │◄────────┐
                       │  (ready to run)      │          │
                       └─────────────────────┘          │
                                 │                       │
                   OS schedules  │   I/O completes /     │
                                 │   lock acquired       │
                                 ▼                       │
                       ┌─────────────────────┐           │
                       │      RUNNING         │           │
                       └─────────────────────┘           │
                          │           │                   │
             I/O wait or  │           │ run() finishes    │
             lock blocked │           │                   │
                          ▼           ▼                   │
                  ┌──────────────┐  ┌──────────────────┐  │
                  │   BLOCKED /  │  │   TERMINATED      │  │
                  │   WAITING    │  │   (dead)          │  │
                  └──────────────┘  └──────────────────┘  │
                          │                                │
                          └────────────────────────────────┘
                            (when block resolves → RUNNABLE)
```

---

## Python GIL — Global Interpreter Lock

```
CPython (the standard Python interpreter) has a GIL:

  "Only ONE Python thread can execute Python bytecode at a time."

  ┌──────────────────────────────────────────────────────────┐
  │                   CPython Process                        │
  │                                                          │
  │   [  GIL  ]                                              │
  │      │                                                   │
  │      ▼                                                   │
  │   Thread A runs ──► Thread A releases GIL ──►           │
  │                                              Thread B runs│
  │                                                          │
  │   Threads TAKE TURNS holding the GIL.                   │
  │   True parallelism on multiple cores: NOT possible       │
  │   for CPU-bound Python threads.                         │
  └──────────────────────────────────────────────────────────┘

CONSEQUENCES:
  CPU-bound tasks:  Threading ≈ serial. Use multiprocessing instead.
  I/O-bound tasks:  Threading IS beneficial — GIL is released during
                    I/O wait (network call, file read, sleep).

GIL is released by:
  - I/O operations
  - time.sleep()
  - C extensions that explicitly release it (e.g., NumPy, regex)
```

---

## Threads Summary Table

```
┌───────────────────────────┬──────────────────────────────────────────┐
│ CONCEPT                   │ KEY FACT                                  │
├───────────────────────────┼──────────────────────────────────────────┤
│ Thread vs. Process        │ Threads share heap; processes don't       │
│ Concurrency vs. Parallelism│ Interleaved vs. simultaneous             │
│ GIL in CPython            │ Only one thread runs Python bytecode at   │
│                           │ a time; released during I/O               │
│ Use threading for         │ I/O-bound work (network, files, DB)       │
│ Use multiprocessing for   │ CPU-bound work (heavy computation)        │
│ Thread creation cost      │ Cheap relative to new process             │
│ Context switch            │ OS decides when to pause/resume threads   │
└───────────────────────────┴──────────────────────────────────────────┘
```
