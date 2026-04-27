# Singleton Pattern

> **The one-line idea:** Ensure a class has **exactly one instance** and provide a global access point to it.

---

## Real-World Analogy — Supreme Court

```
A country has exactly ONE Supreme Court.
It doesn't matter who asks — "Give me the Supreme Court" —
they always get the same institution.

There is no sense in creating a second Supreme Court.
Creating one is expensive and its state must be shared by everyone.
```

---

## When to Use Singleton

```
USE when:
  ✓  The resource is expensive to create (DB connection pool, logger, config loader)
  ✓  Shared state must be consistent across all users (config, cache)
  ✓  Exactly one coordinator makes sense (thread pool, event bus)

AVOID when:
  ✗  You want testability (Singletons make mocking hard)
  ✗  The "single instance" is a design assumption, not a hard requirement
  ✗  It becomes a disguised global variable that couples everything
```

---

## Structure

```
┌──────────────────────────────────────────────────────┐
│                    Singleton                         │
├──────────────────────────────────────────────────────┤
│  - _instance: Singleton  [class variable, private]   │
├──────────────────────────────────────────────────────┤
│  - __init__()             [private constructor]      │
│  + get_instance() → Self  [class method]             │
│  + some_operation()                                  │
└──────────────────────────────────────────────────────┘
```

---

## get_instance() Flow

```
Client A, B, C all call get_instance()

  Client A             Client B             Client C
     │                    │                    │
     └────────────────────┴────────────────────┘
                          │
                          ▼
               ┌──────────────────┐
               │  _instance None? │
               └──────────────────┘
                  YES │      NO │
                      │         └───────────────────────┐
                      ▼                                  ▼
             ┌────────────────┐               ┌──────────────────┐
             │ Create instance│               │ Return existing   │
             │ store in class  │               │ _instance         │
             └────────────────┘               └──────────────────┘
                      │
                      ▼
             Return the new instance

All three clients end up holding a reference to THE SAME object.
```

---

## Thread-Safety Warning

```
Without locks, two threads can both pass the "is None?" check
and each create a separate instance:

  Thread 1: checks _instance → None  ←─ context switch here!
  Thread 2: checks _instance → None
  Thread 2: creates instance (instance = 1st)
  Thread 1: creates instance (instance = 2nd)  ← duplicate!

FIX — Use a lock:

  _lock = threading.Lock()

  @classmethod
  def get_instance(cls):
      if cls._instance is None:         # fast path (no lock)
          with cls._lock:               # slow path (acquire lock)
              if cls._instance is None: # double-check after acquiring
                  cls._instance = cls()
      return cls._instance

This is the "double-checked locking" pattern.
```

---

## Singleton Checklist

```
  □  Is there a genuine reason for exactly one instance?
     If "it's convenient" → use dependency injection instead.

  □  Is the singleton thread-safe (double-checked locking or module-level)?
     If no → race condition risk at startup.

  □  Can you replace the singleton with a mock/stub in tests?
     If no → consider injecting it as an interface instead.
```
