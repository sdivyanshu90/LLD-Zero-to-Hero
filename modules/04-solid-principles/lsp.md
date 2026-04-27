# Liskov Substitution Principle (LSP)

> **The one-line idea:** If `S` is a subtype of `T`, you should be able to use an `S` anywhere a `T` is expected — **without the program behaving incorrectly**.

---

## Real-World Analogy — Vehicle Rental

```
You rent a "Vehicle" from a rental agency.
The contract says:
  - start_engine() works
  - drive(destination) works
  - fuel_gauge() returns remaining fuel percentage

You get handed a Bicycle instead.
  - start_engine() → NotImplementedError  ← CONTRACT BROKEN
  - fuel_gauge()   → always returns 100   ← MISLEADING

A Bicycle is NOT a proper subtype of a motorised Vehicle.
Giving you a Bicycle violates the rental contract.
```

---

## The Four Contract Rules

For `S` to be a proper subtype of `T`:

```
RULE 1 — Preconditions cannot be STRENGTHENED in a subtype
  Parent accepts: amount >= 0
  Child demands:  amount >= 100   ← MORE restrictive = violation
  (The child rejects inputs the parent would have accepted)

RULE 2 — Postconditions cannot be WEAKENED in a subtype
  Parent guarantees: returns a non-empty list
  Child returns:     may return None  ← LESS guaranteed = violation
  (The child promises less than the parent promised)

RULE 3 — Invariants of the parent must be preserved
  Parent invariant: balance is always >= 0
  Child allows:     balance can go negative  ← invariant broken = violation

RULE 4 — Exception specification cannot be broadened
  Parent throws:  InsufficientFundsError only
  Child throws:   DatabaseError, NetworkError, RuntimeError  ← broader = violation
```

---

## The Classic Violation — Square inherits Rectangle

```
+───────────────────────┐
│       Rectangle        │
│  - _width: float       │
│  - _height: float      │
│  + set_width(w)        │
│  + set_height(h)       │
│  + area() → float      │  ← area = _width × _height
└────────────────────────┘
            ▲
            │ (inherits)
+───────────────────────┐
│        Square          │  ← Mathematically, Square IS-A Rectangle?
│  + set_width(w)        │    → overrides to set both sides equal
│  + set_height(h)       │    → overrides to set both sides equal
└────────────────────────┘
```

**Why this violates LSP:**

```
def assert_rectangle_contract(rect: Rectangle):
    rect.set_width(5)
    rect.set_height(4)
    assert rect.area() == 20   # width × height = 5 × 4 = 20

# Works with Rectangle:
r = Rectangle()
assert_rectangle_contract(r)   # ✓ passes

# BREAKS with Square:
s = Square()
assert_rectangle_contract(s)
# After set_width(5): both sides = 5
# After set_height(4): both sides = 4
# area() = 16, not 20   ← ASSERTION FAILS
```

**The geometric IS-A does not mean the computational IS-A holds.**

### Fix — Separate types; relate through common interface

```
        ┌──────────────────────────────┐
        │      <<interface>>           │
        │          Shape               │
        │  + area() → float            │
        └──────────────────────────────┘
                     ▲
          ┌──────────┴──────────┐
          │                     │
   ┌──────────────┐     ┌──────────────┐
   │  Rectangle   │     │   Square     │
   │  set_width() │     │  set_side()  │
   │  set_height()│     │  area()      │
   │  area()      │     └──────────────┘
   └──────────────┘

No substitution between Rectangle and Square — they are siblings.
```

---

## LSP Smell Detector

```
  SMELL 1 — Empty or exception-throwing overrides
    class ReadOnlyFile(File):
        def write(self, data): raise PermissionError
    → File promised write() works. ReadOnlyFile breaks that promise.

  SMELL 2 — Checking type inside a method
    def process(shape: Shape):
        if isinstance(shape, Square):
            ...special handling...
    → If LSP were satisfied, no special handling would be needed.

  SMELL 3 — Narrowing parameter types in override
    Parent:  def process(self, value: Number): ...
    Child:   def process(self, value: int): ...  ← rejects floats parent accepted

  SMELL 4 — Weakening return type
    Parent:  def get_items(self) -> list[Item]: ...
    Child:   def get_items(self) -> list | None: ...  ← caller now needs None check
```

---

## LSP Checklist

```
  □  Can every unit test written for the parent class pass unchanged
     when given a subclass instance?
     If no → LSP is violated.

  □  Does any subclass method throw an exception for a case the
     parent method handles silently?
     If yes → precondition strengthened or exception spec broadened.

  □  Does any subclass override a method with a "do nothing" body?
     If yes → the subtype is not truly a behavioural subtype.

  □  Do callers ever use isinstance() to handle a subtype differently?
     If yes → the subtype is not substitutable.
```
