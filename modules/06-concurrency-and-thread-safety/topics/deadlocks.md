# Deadlocks

> **The one-line idea:** A deadlock is a situation where two or more threads each hold a lock the other needs — all of them blocked forever, waiting for a release that will never come.

---

## Real-World Analogy — Two Stubborn Drivers

```
A two-way road narrows to one lane on a bridge.
Two drivers meet in the middle, facing each other.

  Driver A: "I'm not reversing until you do."
  Driver B: "I'm not reversing until you do."

Both hold their position (their lock).
Both wait for the other to release (give way).
Neither will. Traffic halts forever.

In software:
  Thread 1 holds Lock A, waits for Lock B.
  Thread 2 holds Lock B, waits for Lock A.
```

---

## Classic Deadlock Diagram

```
Thread 1                              Thread 2
  │                                      │
  ▼                                      ▼
acquires Lock A ✓                    acquires Lock B ✓
  │                                      │
  ▼                                      ▼
tries to acquire Lock B ──── BLOCKS ───► waiting...
  │                                      │
  │               waiting...  ◄──────── tries to acquire Lock A
  │                                      │
  ▼                                      ▼
forever blocked                      forever blocked

            ── DEADLOCK ──
```

**The circular wait:**

```
  Thread 1 ──waits for──► Lock B (held by Thread 2)
  Thread 2 ──waits for──► Lock A (held by Thread 1)
```

---

## Four Coffman Conditions

All FOUR must hold simultaneously for a deadlock to occur:

```
  1. MUTUAL EXCLUSION
     At least one resource can only be held by one thread at a time.
     (Locks are inherently mutually exclusive.)

  2. HOLD AND WAIT
     A thread is holding at least one resource and waiting to acquire more.

  3. NO PREEMPTION
     Resources (locks) cannot be forcibly taken away from threads.
     A thread must voluntarily release its lock.

  4. CIRCULAR WAIT
     A set of threads wait in a cycle:
     T1 waits for T2, T2 waits for T3, T3 waits for T1.

Break ANY ONE condition → deadlock cannot occur.
```

---

## Prevention Strategy 1 — Lock Ordering

```
Define a GLOBAL ORDER for acquiring locks.
All threads must acquire locks in the SAME order.

EXAMPLE — Bank Transfer:
  transfer(account_a, account_b, amount):
      ...

  Thread 1: transfer(Account-101, Account-202, 50)
  Thread 2: transfer(Account-202, Account-101, 30)

  Without lock ordering:
    T1 locks 101, T2 locks 202 → DEADLOCK as before.

  WITH lock ordering (always lock lower ID first):
    T1: lock min(101,202)=101 then lock 202  ✓
    T2: lock min(202,101)=101 then lock 202  ✓

    Both threads attempt to acquire 101 first.
    One succeeds; the other waits.
    No cycle → no deadlock.
```

---

## Prevention Strategy 2 — Try-Lock with Timeout

```
Instead of blocking indefinitely, use a timeout:

  def transfer(src_lock, dst_lock, amount):
      acquired = False
      while not acquired:
          if src_lock.acquire(timeout=0.1):
              if dst_lock.acquire(timeout=0.1):
                  try:
                      ...do transfer...
                  finally:
                      dst_lock.release()
                      src_lock.release()
                  acquired = True
              else:
                  src_lock.release()   ← release what we hold, retry later

This breaks HOLD AND WAIT — if we can't get both, we release all and retry.
```

---

## Wait-For Graph — Deadlock Detection

```
Represent which thread is waiting for which lock (resource):

  Thread 1 ──► Lock B ──► Thread 2 ──► Lock A ──► Thread 1

If there is a CYCLE in this graph → DEADLOCK EXISTS.

  T1 → B → T2 → A → T1   ← cycle detected = deadlock confirmed

Operating systems and database engines use this to detect and
break deadlocks by forcibly rolling back one transaction.
```

---

## Deadlock Checklist

```
  □  Do all threads acquire multiple locks in the SAME fixed order?
     If not → circular wait is possible.

  □  Is the amount of time a lock is held minimised?
     Long critical sections increase the chance of contention.

  □  Do you use try-lock with timeout for any multi-lock acquisitions?
     If not → a thread can block indefinitely.

  □  Have you drawn the wait-for graph for your lock acquisition sequence?
     A cycle in the graph = guaranteed deadlock under the right timing.

  □  For Hard LLD problems: is a lock-free alternative possible?
     (queue.Queue is already thread-safe; threading.Event for signalling)
```
