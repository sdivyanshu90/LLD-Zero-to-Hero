# Builder Pattern

> **The one-line idea:** Separate the **construction** of a complex object from its **representation** — build it step by step using a fluent interface, then produce the finished product.

---

## Real-World Analogy — Custom Laptop Order

```
You walk into a laptop configurator website:

  Step 1: Choose CPU:         Intel i7
  Step 2: Choose RAM:         16 GB
  Step 3: Choose Storage:     512 GB SSD
  Step 4: Choose GPU:         NVIDIA 4060
  Step 5: Choose Display:     4K OLED
  Step 6: Confirm:            [ BUILD MY LAPTOP ]

You configure step-by-step. You only get the final product at the end.
The assembly factory (Builder) manages all the complexity.
```

---

## The Problem Without Builder

```
# Constructor hell — what does each argument mean?
query = Query("users", ["id","name","email"], {"age": 18}, "name", "ASC", 10, 0)

# With Builder — self-documenting, order-independent:
query = (QueryBuilder()
    .from_table("users")
    .select("id", "name", "email")
    .where("age", ">", 18)
    .order_by("name", ascending=True)
    .limit(10)
    .offset(0)
    .build())
```

---

## Structure — Fluent QueryBuilder

```
┌─────────────────────────────────────────────────────────┐
│                    QueryBuilder                         │
├─────────────────────────────────────────────────────────┤
│  - _table: str                                          │
│  - _columns: list[str]                                  │
│  - _conditions: list[tuple]                             │
│  - _order_by: str | None                                │
│  - _limit: int | None                                   │
│  - _offset: int                                         │
├─────────────────────────────────────────────────────────┤
│  + from_table(table: str) → Self                        │
│  + select(*columns: str) → Self                         │
│  + where(col, op, value) → Self   (returns self → chain)│
│  + order_by(col, ascending) → Self                      │
│  + limit(n: int) → Self                                 │
│  + offset(n: int) → Self                                │
│  + build() → Query                  (terminal step)     │
└─────────────────────────────────────────────────────────┘
```

**The fluent interface chain:**

```
  QueryBuilder()
       │
       ▼
  .from_table("users")  → returns self
       │
       ▼
  .select("id","name")  → returns self
       │
       ▼
  .where("age",">",18)  → returns self
       │
       ▼
  .limit(10)            → returns self
       │
       ▼
  .build()              → returns final Query object
```

---

## Constructor vs. Builder Readability

```
WITHOUT Builder — positional args, hard to read:

  Pizza("large", True, True, False, True, False, True, "thin")
  #      size    cheese extra-cheese  onion  pepper  tomato crust

WITH Builder — named steps, intent is clear:

  pizza = (PizzaBuilder()
      .size("large")
      .add_cheese(extra=True)
      .add_pepper()
      .add_tomato()
      .crust("thin")
      .build())
```

---

## When to Use / Avoid

```
USE when:
  ✓  Object construction involves many optional parameters
  ✓  The same construction process needs to produce different representations
  ✓  You want to prevent partially-initialised objects

AVOID when:
  ✗  The object is simple with only 1-2 required fields
  ✗  All fields are always required (use a regular constructor)
  ✗  The builder adds verbosity with no readability benefit
```

---

## Builder Checklist

```
  □  Are callers confused about argument order in the constructor?
     If yes → Builder is the right fit.

  □  Does the build() method validate the configuration before
     returning the object?
     If not → add validation there to prevent invalid objects.

  □  Do all "setter" methods return self to enable chaining?
     If no → the fluent interface is broken.
```
