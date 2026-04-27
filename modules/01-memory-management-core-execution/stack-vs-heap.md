# Stack vs. Heap

> **The one-line idea:** The **stack** is scratchpad memory for the *current task*; the **heap** is the *shared warehouse* where objects live as long as someone still needs them.

---

## Real-World Analogy

Imagine a busy office building:

```
┌─────────────────────────────────────────────────────┐
│                    OFFICE BUILDING                  │
│                                                     │
│  ┌──────────────────────┐  ┌─────────────────────┐  │
│  │   YOUR DESK (Stack)  │  │  STORAGE ROOM (Heap)│  │
│  │                      │  │                     │  │
│  │  • Sticky notes for  │  │  • Big boxes of     │  │
│  │    the current task  │  │    shared resources │  │
│  │  • Cleared when you  │  │  • Stays until      │  │
│  │    finish the task   │  │    nobody claims it │  │
│  │  • Small & fast      │  │  • Large & flexible │  │
│  └──────────────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

- When you are on a phone call (executing a function), you jot notes on your desk (stack frame).
- When the call ends, you wipe the desk — those local notes are gone.
- But if you wrote something in the storage room (heap), it persists until the janitor (garbage collector) decides nobody needs it.

---

## Memory Layout Diagram

```
HIGH ADDRESS
┌──────────────────────────────┐
│           STACK              │  ← grows downward
│  ┌────────────────────────┐  │
│  │  Frame: main()         │  │
│  │   x = [ref → 0x1A2B]   │  │
│  ├────────────────────────┤  │
│  │  Frame: process(x)     │  │  ← currently executing
│  │   data = [ref → 0x1A2B]│  │
│  └────────────────────────┘  │
│              ↓ grows         │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│  (free space)                │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│              ↑ grows         │
│  ┌────────────────────────┐  │
│  │         HEAP           │  │  ← grows upward
│  │  0x1A2B: [1, 2, 3]     │  │
│  │  0x3C4D: "hello"       │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
LOW ADDRESS
```

---

## Key Properties Side-by-Side

| Property | Stack | Heap |
|---|---|---|
| **Allocation speed** | O(1) — just move the stack pointer | Slower — allocator must find free space |
| **Lifetime** | Tied to function call duration | Lives until last reference is gone |
| **Size** | Small (typically 1–8 MB) | Large (limited by OS/RAM) |
| **Who manages it** | CPU / calling convention | Runtime / Garbage Collector |
| **Thread ownership** | Each thread has its own stack | All threads share one heap |
| **Access pattern** | LIFO — last in, first out | Random access |

---

## What Goes Where?

```
def greet(name):             # <-- name is a local variable → on the Stack
    message = "Hello, "      # <-- message is a local variable → on the Stack
    result = message + name  # <-- the NEW string object lives on the Heap
    return result            # <-- the Stack frame is destroyed; string on Heap survives
                             #     (if the caller stores the return value)
```

**Rule of thumb:**
- Local variable *names* and small cached integers → stack frame.
- All objects (lists, dicts, class instances, strings) → heap.

---

## Call Stack Walkthrough

```
Program execution →

main()
  └─ calls process()
        └─ calls validate()
              └─ calls is_empty()   ← top of stack right now

Stack at this moment:
┌─────────────────┐  ← top (most recent)
│  is_empty()     │
├─────────────────┤
│  validate()     │
├─────────────────┤
│  process()      │
├─────────────────┤
│  main()         │  ← bottom (program entry)
└─────────────────┘

When is_empty() returns → its frame is popped.
When validate() returns → its frame is popped.
... and so on.
```

> **Stack Overflow** happens when the stack runs out of space — most commonly through runaway recursion.

---

## The Full Picture

```
┌──────────────────────────────────────────────────────────────┐
│                        PROGRAM RUN                           │
│                                                              │
│  ┌─────────┐    calls     ┌───────────────────────────────┐  │
│  │  Stack  │◄────────────►│           Heap                │  │
│  │         │  references  │                               │  │
│  │ Frame N │─────────────►│  Objects (instances, lists,   │  │
│  │ Frame 2 │              │  dicts, strings, closures...) │  │
│  │ Frame 1 │              │                               │  │
│  └─────────┘              └───────────────────────────────┘  │
│                                   ▲                          │
│                                   │ frees when unreachable   │
│                           ┌───────────────┐                  │
│                           │    Garbage    │                  │
│                           │   Collector   │                  │
│                           └───────────────┘                  │
└──────────────────────────────────────────────────────────────┘
```
