# Garbage Collection

> **The one-line idea:** The garbage collector is the **building janitor** — it removes objects from the heap that nobody in the program holds a reference to anymore.

---

## Why GC is Needed

Programs create objects continuously. Without cleanup:

```
Iteration 1:  heap = [ obj_A ]
Iteration 2:  heap = [ obj_A, obj_B ]
Iteration 3:  heap = [ obj_A, obj_B, obj_C ]
...
Iteration N:  heap = [ obj_A ... obj_N ]  ← OutOfMemoryError
```

The GC reclaims memory for objects that are **unreachable** — no live code holds a reference to them.

---

## Mechanism 1 — Reference Counting

Every object keeps a counter: *"how many names or slots currently point at me?"*

```
Step 1: x = [1, 2, 3]
        ┌───┐
        │ x │──────────► [1,2,3]  refcount = 1
        └───┘

Step 2: y = x
        ┌───┐
        │ x │──────────► [1,2,3]  refcount = 2
        └───┘                         ▲
        ┌───┐                         │
        │ y │─────────────────────────┘
        └───┘

Step 3: x = None   (x stops pointing at the list)
        refcount of [1,2,3] drops to 1  → still alive (y holds it)

Step 4: y = None
        refcount of [1,2,3] drops to 0  → FREED immediately
```

> **Advantage:** Objects are freed the instant they are no longer needed — no unpredictable pauses.

---

## The Fatal Flaw — Reference Cycles

Reference counting fails when two objects point at each other:

```
┌────────────┐       ┌────────────┐
│   node_A   │──────►│   node_B   │
│ refcount=1 │◄──────│ refcount=1 │
└────────────┘       └────────────┘
     ▲
     │
    (the only external variable holding node_A goes out of scope)

After the outer reference is dropped:
  node_A.refcount = 1  (node_B still points at it)
  node_B.refcount = 1  (node_A still points at it)

Both have refcount > 0 → reference counting cannot free them.
They are LEAKED until the cyclic collector runs.
```

---

## Mechanism 2 — Cyclic Garbage Collector (Mark and Sweep)

Python's second layer handles cycles:

```
Phase 1 — MARK (find all reachable objects starting from GC roots)

  GC Roots (globals, stack frames, modules)
       │
       ├──► obj_1  ──► obj_3
       │                 └──► obj_5
       └──► obj_2

  Marked as reachable: { obj_1, obj_2, obj_3, obj_5 }

Phase 2 — SWEEP (collect everything not marked)

  All objects on heap:  { obj_1, obj_2, obj_3, obj_4, obj_5, obj_6 }
  Reachable:            { obj_1, obj_2, obj_3,        obj_5        }
  Garbage (collected):  {                      obj_4,        obj_6 }
                              ↑ cycle              ↑ just unreachable
```

---

## Python's Three Generations

Python's cyclic GC uses a **generational** strategy based on the observation that *most objects die young*:

```
┌──────────────────────────────────────────────────────────┐
│                   GENERATIONAL GC                        │
│                                                          │
│  Generation 0   Generation 1   Generation 2             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐             │
│  │ Newborn  │──►│ Survived │──►│Long-lived│             │
│  │ objects  │   │ one GC   │   │ objects  │             │
│  │          │   │          │   │          │             │
│  │Collected │   │Collected │   │Collected │             │
│  │ OFTEN    │   │ less     │   │ rarely   │             │
│  │ (fast)   │   │ often    │   │          │             │
│  └──────────┘   └──────────┘   └──────────┘             │
│                                                          │
│  Most garbage is in Gen 0 → cheap to collect frequently  │
└──────────────────────────────────────────────────────────┘
```

The older a generation, the less frequently it is checked — saving CPU time.

---

## Two-Mechanism Summary

```
┌──────────────────────┬────────────────────────────────────────────┐
│ Mechanism            │ What it handles                            │
├──────────────────────┼────────────────────────────────────────────┤
│ Reference Counting   │ Objects with no cycles (the vast majority) │
│                      │ Freed immediately when refcount drops to 0 │
├──────────────────────┼────────────────────────────────────────────┤
│ Cyclic GC            │ Objects in reference cycles                │
│                      │ Runs periodically, not immediately         │
└──────────────────────┴────────────────────────────────────────────┘
```

---

## Common Memory Pitfalls

| Pitfall | What happens | Fix |
|---|---|---|
| Circular references in custom classes | Memory not freed by refcount alone | Use `weakref` for back-references |
| Storing large objects in module globals | They live for the entire program | Use `del` explicitly or limit scope |
| Caches without size limits | Memory grows unboundedly | Use `functools.lru_cache(maxsize=N)` |
| Event listeners keeping receivers alive | Hidden references block GC | Register listeners with `weakref` |

---

## weakref — Breaking Cycles Intentionally

```
A strong reference:   node_A → node_B → node_A  (cycle, leaked)

A weak reference:     node_A ──strong──► node_B
                      node_B ──weak────► node_A   (doesn't count for refcount)

  import weakref
  node_A.back = weakref.ref(node_B)   # weak reference — doesn't increment refcount
  # When node_A has no more strong references, it's freed even though node_B.back exists.
  # node_B.back() returns None after node_A is collected.
```
