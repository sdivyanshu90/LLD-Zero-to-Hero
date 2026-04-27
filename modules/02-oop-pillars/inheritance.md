# Inheritance

> **The one-line idea:** A child class is a **specialized version** of its parent — it IS-A more specific kind of the parent.

---

## Real-World Analogy — Animal Kingdom

```
                        ┌─────────┐
                        │ Animal  │   ← general concept
                        │         │
                        │ eat()   │
                        │ sleep() │
                        │ breathe │
                        └─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         ┌─────────┐    ┌─────────┐    ┌─────────┐
         │   Dog   │    │   Cat   │    │   Bird  │
         │         │    │         │    │         │
         │ bark()  │    │ meow()  │    │  fly()  │
         │ fetch() │    │ purr()  │    │ sing()  │
         └─────────┘    └─────────┘    └─────────┘
         IS-A Animal   IS-A Animal    IS-A Animal
```

A `Dog` inherits `eat()`, `sleep()`, `breathe()` from `Animal`. It *extends* that foundation with dog-specific behavior — it doesn't rewrite it.

---

## Inheritance Hierarchy Diagram

```
           ┌────────────────────────────────────────┐
           │              Account                   │
           │  - account_number: str                 │
           │  - balance: float                      │
           │  + deposit(amount)                     │
           │  + get_balance() → float               │
           └────────────────────────────────────────┘
                            ▲
             ┌──────────────┴──────────────┐
             │                             │
  ┌──────────────────────┐    ┌────────────────────────┐
  │    SavingsAccount    │    │    CheckingAccount      │
  │                      │    │                        │
  │  - interest_rate     │    │  - overdraft_limit     │
  │  + apply_interest()  │    │  + withdraw(amount)    │
  │  + withdraw(amount)  │    │    (allows overdraft)  │
  └──────────────────────┘    └────────────────────────┘
```

Both subclasses reuse `deposit()` and `get_balance()` for free. Each adds its own specialisation.

---

## IS-A vs. HAS-A — The Critical Test

This is the most common inheritance mistake. Before inheriting, ask:  
**"Is [Child] truly a kind of [Parent]?"**

```
✅  CORRECT IS-A relationships:
    Dog IS-A Animal              → Dog inherits Animal
    SavingsAccount IS-A Account  → SavingsAccount inherits Account
    Square IS-A Shape            → Square inherits Shape (careful with LSP!)

❌  WRONG IS-A (really HAS-A):
    Car IS-A Engine?             → No. Car HAS-A Engine. Use composition.
    Person IS-A Address?         → No. Person HAS-A Address. Use composition.
    Stack IS-A List?             → Debatable. Stack HAS-A internal list is safer.
```

---

## Method Resolution Order (MRO)

When a method is called, Python searches in a specific order:

```
class A:
    def hello(self): ...

class B(A):
    def hello(self): ...   ← overrides A's hello

class C(B):
    pass                   ← no hello defined

c = C()
c.hello()

MRO search order: C → B → A → object

  C: no hello defined → keep looking
  B: hello found!    → call B.hello()
```

For multiple inheritance, Python uses the **C3 Linearization** algorithm:

```
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

MRO for D: D → B → C → A → object

  Visualized:
  D
  ├── B ──► A
  └── C ──► A

  C3 ensures A is only visited once, after both B and C.
```

---

## When NOT to Use Inheritance

```
ANTI-PATTERN — Inheritance for code reuse alone:

  class DatabaseUtils:
      def connect(self): ...
      def query(self): ...

  class UserRepository(DatabaseUtils):  # WRONG: UserRepo IS-A DatabaseUtil?
      pass

CORRECT — Composition for code reuse:

  class UserRepository:
      def __init__(self, db: Database):
          self._db = db   # HAS-A database connection

      def find_by_id(self, user_id):
          return self._db.query(f"SELECT * FROM users WHERE id={user_id}")
```

> **Rule:** Use inheritance for *type relationships*. Use composition for *behaviour reuse*.

---

## Inheritance Anti-Pattern Gallery

```
ANTI-PATTERN 1 — Deep hierarchies:
  Animal → Vertebrate → Mammal → Carnivore → Cat → DomesticCat → PersianCat
  ← 7 levels. Any change in the middle breaks everything below it.
  Fix: Prefer shallow hierarchies (max 2–3 levels) + composition.

ANTI-PATTERN 2 — Inheriting to get access to protected methods:
  class MyList(list):   # just to use list._resize()? NO.
  Fix: Wrap, don't extend.

ANTI-PATTERN 3 — Overriding a method to do nothing:
  class NullLogger(Logger):
      def log(self, msg): pass   ← silently swallows everything
  This likely violates LSP (see Module 4). Consider whether Logger
  is the right abstraction.
```

---

## Summary

```
USE inheritance when:                  AVOID inheritance when:
─────────────────────                  ──────────────────────
Child IS-A parent (genuinely)          You just want to reuse methods
Shared behaviour belongs in parent     The hierarchy is deeper than 3 levels
Subtype substitution is safe (LSP)     You need multiple "dimensions" of variation
```
