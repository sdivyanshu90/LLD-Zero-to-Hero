# Strategy Pattern

> **The one-line idea:** Define a family of algorithms, encapsulate each one, and make them **interchangeable** at runtime — without modifying the code that uses them.

---

## Real-World Analogy — Navigation App

```
You open Google Maps and select a destination.
Maps asks: "How do you want to travel?"

  [ Walking ]   [ Cycling ]   [ Driving ]   [ Public Transit ]

Each option is a different STRATEGY for the same goal: getting from A to B.
You can switch between them without Maps re-writing its routing logic.
```

---

## Structure

```
              ┌──────────────────────────────────────────┐
              │              SortContext                  │
              │  - _strategy: SortStrategy                │
              │  + set_strategy(strategy: SortStrategy)   │
              │  + sort(data: list) → list                │
              │    → delegates to self._strategy.execute()│
              └──────────────────────────────────────────┘
                               │ uses
                               ▼
              ┌──────────────────────────────────────────┐
              │           <<interface>>                   │
              │           SortStrategy                    │
              │  + execute(data: list) → list             │
              └──────────────────────────────────────────┘
                               ▲
              ┌────────────────┼──────────────────┐
              │                │                  │
  ┌───────────────────┐  ┌──────────────────┐  ┌─────────────────┐
  │   QuickSort       │  │   MergeSort      │  │  BubbleSort     │
  │  execute(data)    │  │  execute(data)   │  │  execute(data)  │
  │  → O(n log n)     │  │  → O(n log n)    │  │  → O(n²)        │
  │    avg, in-place  │  │    stable, extra │  │    simple       │
  └───────────────────┘  └──────────────────┘  └─────────────────┘
```

---

## Runtime Switching

```
context = SortContext()

# Large dataset → use QuickSort
context.set_strategy(QuickSort())
result = context.sort(million_records)

# Nearly sorted data → use BubbleSort (O(n) for nearly sorted)
context.set_strategy(BubbleSort())
result = context.sort(small_nearly_sorted)

# Need stable sort → use MergeSort
context.set_strategy(MergeSort())
result = context.sort(records_with_equal_keys)

The SAME context object, different algorithm each time.
```

---

## Strategy vs. Inheritance Comparison

```
WITHOUT Strategy — algorithm baked into the class:

  class Sorter:
      def sort(self, data, algorithm: str):
          if algorithm == "quick":   ...
          elif algorithm == "merge": ...
          elif algorithm == "bubble": ...
          # New algorithm? MODIFY this class.

WITH Strategy — algorithm injected:

  class Sorter:
      def __init__(self, strategy: SortStrategy):
          self._strategy = strategy

      def sort(self, data: list) → list:
          return self._strategy.execute(data)   # never changes

  New algorithm? Write a new SortStrategy class. Sorter stays closed.
```

---

## When to Use / Avoid

```
USE when:
  ✓  Multiple related algorithms that differ only in behaviour
  ✓  You want to switch algorithms at runtime
  ✓  You want to eliminate conditional branching based on algorithm type

AVOID when:
  ✗  There is only one algorithm and no plans for alternatives
  ✗  The algorithms are trivial one-liners (just pass a function/lambda)
```

---

## Strategy Checklist

```
  □  Is the Strategy interface single-purpose (one execute/run method)?
     If it has 5 methods → it's not a strategy, it's a collaborator.

  □  Does the Context hold a reference to the interface, not a concrete class?
     If not → you haven't actually applied DIP.

  □  Can you swap strategies without touching the Context?
     If not → the strategy is leaking details into the Context.
```
