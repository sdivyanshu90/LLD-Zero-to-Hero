# Race Conditions

> **The one-line idea:** A race condition occurs when the program's output depends on the **timing and order** of threads' execution — producing unpredictable, often wrong results.

---

## Classic Example — Lost Counter Increment

```
Expected: Two threads each increment a counter 100,000 times.
Final value should be 200,000.

Reality: Final value is often anywhere from 100,000 to ~190,000.

WHY?
```

---

## Bytecode-Level Interleaving

```
counter = 0

Python compiles "counter += 1" into THREE bytecode steps:

  LOAD   counter    (read current value into register)
  ADD    1          (add 1 to the register)
  STORE  counter    (write result back to memory)

Thread 1 and Thread 2 can interleave these steps:

  Time:    Thread 1          Thread 2        counter
  ─────────────────────────────────────────────────
   t1:   LOAD  counter                         0
   t2:                    LOAD  counter        0  ← BOTH read 0!
   t3:   ADD   1                               0
   t4:                    ADD   1              0
   t5:   STORE counter (=1)                    1
   t6:                    STORE counter (=1)   1  ← Thread 2 OVERWRITES!

Both threads incremented, but counter only went from 0 to 1.
ONE INCREMENT WAS LOST.
```

---

## Three Conditions for a Race Condition

```
All three must be true simultaneously:

  1. SHARED MUTABLE STATE
     Multiple threads can access and modify the same variable.
                    │
  2. NON-ATOMIC OPERATION
     The modification involves multiple steps (read → modify → write).
                    │
  3. NO SYNCHRONISATION
     There is no mechanism preventing concurrent access during those steps.

Remove any one condition → no race condition.
  Option A: Make state immutable (remove condition 1)
  Option B: Use an atomic operation (remove condition 2)
  Option C: Use a lock (remove condition 3)
```

---

## Four Types of Race Conditions

### Type 1 — Lost Update (most common)

```
T1 reads value 5, T2 reads value 5, T1 writes 6, T2 writes 6.
T1's update is lost. Final value is 6, not 7.

  T1: read(5) ──► add(1) ──► write(6)
  T2: read(5) ──────────────────────────► add(1) ──► write(6)
                                                        ↑ overwrites T1
```

### Type 2 — Dirty Read

```
T1 is in the middle of updating a multi-field object.
T2 reads the object between T1's writes → sees inconsistent state.

  T1: write(name="Alice") ──► write(age=30)
  T2:                    read(name="Alice", age=25)  ← old age!
```

### Type 3 — Check-Then-Act

```
T1 checks a condition, then acts. Between check and act,
T2 changes the condition → T1's action is now invalid.

  T1: check(balance >= 100) → True ──────────────────► deduct(100)
  T2:                         check(balance >= 100) → True ──► deduct(100)
                               ↑ both pass the check!
                               Both deduct, but balance was only 100.
```

### Type 4 — Non-Repeatable Read

```
T1 reads a value twice. T2 modifies it between the two reads.
T1 sees different values for the same data in one logical operation.
```

---

## Race Condition Checklist

```
  □  Is there shared mutable state accessed by multiple threads?
  □  Is the access non-atomic (read-modify-write pattern)?
  □  Are there check-then-act patterns without a lock?
  □  Is any object being partially constructed and shared before
     construction completes?

If any YES → protect with a lock (see mutexes-and-locks.md).
```
