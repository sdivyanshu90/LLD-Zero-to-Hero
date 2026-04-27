# Mutexes and Locks

> **The one-line idea:** A mutex (mutual exclusion lock) ensures that only **one thread at a time** can execute a critical section — turning a non-atomic multi-step operation into an effectively atomic one.

---

## Real-World Analogy — Single-Occupancy Restroom

```
A single-occupancy restroom has ONE key on a hook by the door.

Thread A arrives → takes the key → enters → does its business.

Thread B arrives while Thread A is inside → no key → WAITS outside.

Thread A finishes → puts key back on hook.

Thread B takes the key → enters.

The key = the lock. The restroom = the critical section.
Only one person inside at a time, by design.
```

---

## Lock Flow Diagram

```
Thread arrives at critical section:

  ┌─────────────────────┐
  │  Is the lock free?   │
  └─────────────────────┘
         │         │
        YES        NO
         │         │
         ▼         ▼
  Acquire lock   Block and wait
  (lock is now   until lock is
   taken)         released
         │
         ▼
  Execute critical section
         │
         ▼
  Release lock
         │
         ▼
  (waiting threads compete to acquire)
```

---

## Critical Section Scope

```
SCOPE TOO WIDE — Kills concurrency (threads wait for unrelated work):

  with lock:
      data = fetch_from_database()        ← slow I/O inside lock!
      processed = expensive_computation() ← CPU work inside lock!
      result = process(processed)
      shared_cache[key] = result          ← only this needs the lock

SCOPE TOO NARROW — Creates race conditions (misses shared state):

  data = fetch_from_database()
  processed = expensive_computation()
  result = process(processed)
  with lock:
      # forgot: check if key already exists before writing!
      shared_cache[key] = result

SCOPE JUST RIGHT — Lock wraps only the access to shared state:

  data = fetch_from_database()           ← outside lock (safe, no shared state)
  processed = expensive_computation()   ← outside lock (safe)
  result = process(processed)
  with lock:                             ← lock only around shared write
      shared_cache[key] = result
```

---

## Lock Types Reference

```
┌────────────────┬──────────────────────────────────────────────────────────┐
│   LOCK TYPE    │ DESCRIPTION AND USE CASE                                 │
├────────────────┼──────────────────────────────────────────────────────────┤
│ Mutex          │ Basic mutual exclusion. One thread at a time.             │
│ (threading.Lock│ Fastest, simplest. Use for most shared state protection. │
│  in Python)    │ WARNING: not reentrant — a thread cannot acquire it twice.│
├────────────────┼──────────────────────────────────────────────────────────┤
│ RLock          │ Reentrant lock. Same thread can acquire multiple times.   │
│(threading.RLock│ Use when recursive functions or nested calls need the     │
│  in Python)    │ same lock. Must release as many times as acquired.        │
├────────────────┼──────────────────────────────────────────────────────────┤
│ RWLock         │ Separate read and write locks.                            │
│ (third-party   │ Multiple readers allowed simultaneously.                  │
│  or manual)    │ Only one writer, and only when no readers are active.     │
│                │ Use for read-heavy shared data structures.                │
├────────────────┼──────────────────────────────────────────────────────────┤
│ Semaphore      │ Counter-based. Allows N threads into a section at once.   │
│(threading.     │ Use to limit resource pool access (e.g., max 5 DB conns).│
│ Semaphore(N))  │                                                           │
├────────────────┼──────────────────────────────────────────────────────────┤
│ Condition      │ Combines a lock with a wait/notify mechanism.             │
│(threading.     │ Use when a thread must wait until a condition is met      │
│ Condition)     │ (e.g., producer/consumer queue coordination).             │
└────────────────┴──────────────────────────────────────────────────────────┘
```

---

## Always Use Context Manager

```
WRONG — easy to forget release on exception:
  lock.acquire()
  try:
      ...shared state access...
  finally:
      lock.release()

RIGHT — context manager handles release automatically:
  with lock:
      ...shared state access...
  # Lock is ALWAYS released, even if an exception is raised.
```

---

## Mutex Checklist

```
  □  Is the critical section as SMALL as possible?
     Move all work that doesn't touch shared state OUTSIDE the lock.

  □  Are you using `with lock:` (context manager)?
     Never rely on manual acquire/release — exceptions skip the release.

  □  Are you using a regular Lock in a recursive function that acquires
     the same lock? → Switch to RLock to prevent deadlock.

  □  Does releasing the lock happen on ALL code paths?
     Context manager guarantees this. Manual acquire/release does not.

  □  Are you using a Semaphore to limit access to a pool (e.g., DB connections)?
     If you need exactly 1 → use Lock. If N > 1 → Semaphore.
```
