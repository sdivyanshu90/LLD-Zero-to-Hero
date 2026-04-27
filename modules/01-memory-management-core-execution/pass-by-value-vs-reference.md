# Pass-by-Value vs. Pass-by-Reference

> **The one-line idea:** **Value** — you hand someone a *photocopy*. **Reference** — you hand someone the *address* of the original.

---

## The Spectrum of Passing Styles

```
              COPY                         ALIAS
   ┌──────────────────────┐     ┌──────────────────────┐
   │   Pass-by-VALUE      │     │  Pass-by-REFERENCE   │
   │                      │     │                      │
   │  caller's var ──► X  │     │  caller's var ──► X  │
   │  callee's var ──► X' │     │  callee's var ──► X  │
   │       (copy)         │     │    (same object!)    │
   └──────────────────────┘     └──────────────────────┘
      Changing X' does NOT         Changing X changes
      affect caller's X            what caller sees
```

---

## Python's Actual Model: Call-by-Sharing

Python does neither pure value nor pure reference. It uses **call-by-sharing** (also called pass-by-object-reference):

### Scenario A — Immutable Object (int, str, tuple)

```
  Caller:  x = 42
           ┌───┐
           │ x │──────────────► [42] (heap)
           └───┘

  After calling f(x):
           ┌───┐
           │ x │──────────────► [42] (heap) ← unchanged
           └───┘
           ┌─────────┐
           │ local n │──────────► [42]  (callee got the same reference)
           └─────────┘
           After n = 99 inside f():
           │ local n │──────────► [99]  (rebinding — caller's x untouched)
```

Immutable objects cannot be mutated, so the caller's variable is always safe.

---

### Scenario B — Mutable Object (list, dict)

```
  Caller:  items = [1, 2, 3]
           ┌───────┐
           │ items │──────────► [1, 2, 3] (heap, address 0xABCD)
           └───────┘

  After calling append_ten(items):
           ┌───────────┐
           │ local lst │──────► [1, 2, 3] (SAME address 0xABCD)
           └───────────┘
           lst.append(10) mutates the heap object directly →
           [1, 2, 3, 10]
           Caller's items now sees [1, 2, 3, 10]  ← SURPRISE if unprepared!
```

Both `items` and `lst` point to the **same object in memory**.

---

## The Key Test — Two Types of Actions

| Action inside the function | Effect on caller's variable |
|---|---|
| **Rebind** the parameter (`n = 99`) | No effect — only the local name moves |
| **Mutate** through the reference (`lst.append(10)`) | Caller sees the change |

---

## Visual Decision Tree

```
Function receives a variable
         │
         ▼
  Is the object mutable?
  (list, dict, set, custom class)
         │
    YES  │  NO (int, str, tuple, frozenset)
         │         │
         ▼         ▼
  Does the function    Mutation is impossible.
  mutate the object?   Rebinding is invisible
  (append, update,     to caller. Completely safe.
   setitem, etc.)
         │
    YES  │  NO (only rebinding)
         │         │
         ▼         ▼
  Caller SEES    Caller CANNOT
  the change     see the change
```

---

## Defensive Patterns

```
# Pattern 1 — Defensive copy (protect caller from mutation)
def process(items):
    safe = list(items)   # work on a copy
    safe.append(99)
    return safe

# Pattern 2 — Explicit intent via naming convention
def sort_in_place(data):   # name signals mutation is intentional
    data.sort()

# Pattern 3 — Return a new value (functional style)
def with_appended(items, value):
    return items + [value]  # original untouched
```

---

## Common Surprises

```
SURPRISE 1 — Default mutable argument (infamous Python gotcha):

  def add_item(item, collection=[]):   # ← [] is created ONCE at definition time
      collection.append(item)
      return collection

  add_item(1)  →  [1]
  add_item(2)  →  [1, 2]   ← NOT [2]! The same list is reused.

  FIX:
  def add_item(item, collection=None):
      if collection is None:
          collection = []
      collection.append(item)
      return collection

SURPRISE 2 — Nested mutable objects in copy:

  import copy
  original = [[1, 2], [3, 4]]
  shallow = list(original)        # copies outer list, NOT inner lists
  shallow[0].append(99)
  print(original)                 # [[1, 2, 99], [3, 4]] ← original changed!

  FIX for deep independence:
  deep = copy.deepcopy(original)
```
