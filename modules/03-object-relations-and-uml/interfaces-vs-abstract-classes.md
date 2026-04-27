# Interfaces vs. Abstract Classes

> **The one-line idea:** Interface = a *pure contract* (what you can do). Abstract Class = a *partial implementation* (some scaffolding + mandatory overrides).

---

## Real-World Analogy

```
INTERFACE — like a job description posting:
  "Must be able to: drive a vehicle, navigate a route, handle payments."
  The posting doesn't care HOW you drive, just THAT you can.

ABSTRACT CLASS — like a franchise operations manual:
  "Here is how to greet customers (shared, already done for you),
   but you decide what food to serve (abstract — you implement it)."
```

---

## Interface (Protocol / ABC with all abstract methods)

```
                    ┌─────────────────────────────────┐
                    │         <<interface>>            │
                    │         Drawable                 │
                    │                                  │
                    │  + draw() → None   [abstract]    │
                    │  + resize(factor) → None [abst.] │
                    │  + get_bounds() → Rect  [abst.]  │
                    └─────────────────────────────────┘
                                   ▲
              .......................│.......................
              ·                    ·                     ·
              ▼                    ▼                     ▼
  ┌───────────────────┐  ┌──────────────────┐  ┌──────────────────┐
  │      Circle       │  │    Rectangle     │  │     SVGPath      │
  │  draw()           │  │  draw()          │  │  draw()          │
  │  resize(factor)   │  │  resize(factor)  │  │  resize(factor)  │
  │  get_bounds()     │  │  get_bounds()    │  │  get_bounds()    │
  └───────────────────┘  └──────────────────┘  └──────────────────┘

Dotted line (......►) = "implements" relationship
```

**Properties of an Interface:**
- No shared state (no instance variables in the contract)
- No implemented methods (all abstract)
- A class can implement **multiple** interfaces simultaneously
- Defines *what* without *how*

---

## Abstract Class

```
                ┌──────────────────────────────────────────┐
                │           <<abstract>>                   │
                │            Report                        │
                │                                          │
                │  _title: str                             │ ← shared state
                │  _created_at: datetime                   │ ← shared state
                │                                          │
                │  + __init__(title)          [concrete]   │ ← shared behaviour
                │  + get_metadata() → dict    [concrete]   │ ← shared behaviour
                │  + generate() → str         [abstract]   │ ← subclass must implement
                │  + format_header() → str    [abstract]   │ ← subclass must implement
                └──────────────────────────────────────────┘
                                   ▲
                    ┌──────────────┴──────────────┐
                    │                             │
          ┌─────────────────┐         ┌──────────────────────┐
          │   PDFReport     │         │     CSVReport         │
          │  generate()     │         │  generate()           │
          │  format_header()│         │  format_header()      │
          └─────────────────┘         └──────────────────────┘

Solid line (──────►) = "inherits" relationship
```

**Properties of an Abstract Class:**
- Can have instance variables (shared state)
- Can have concrete (implemented) methods — shared by all subclasses
- Can have abstract methods — subclasses must override them
- A class can inherit from **only one** abstract class (in most languages; Python allows multiple)

---

## Decision Matrix

```
Ask these questions to decide:

  Does the contract need any shared STATE (instance variables)?
       │                         │
      YES                       NO
       │                         │
       ▼                         ▼
  Abstract Class             Either works

  Does the contract need any SHARED BEHAVIOUR (concrete methods)?
       │                         │
      YES                       NO
       │                         │
       ▼                         ▼
  Abstract Class             Interface preferred

  Will a class need to satisfy MULTIPLE contracts simultaneously?
       │                         │
      YES                       NO
       │                         │
       ▼                         ▼
  Use Interfaces             Either works
  (implement many)
```

---

## Concrete Comparison

```
┌──────────────────┬────────────────────────────┬───────────────────────────┐
│ FEATURE          │ INTERFACE (Protocol/ABC)    │ ABSTRACT CLASS            │
├──────────────────┼────────────────────────────┼───────────────────────────┤
│ Instance vars    │ No                         │ Yes                       │
│ Concrete methods │ No (all abstract)           │ Yes                       │
│ Multiple inherit │ Yes — implement many        │ Limited — one parent      │
│ Purpose          │ "Can do X" capability       │ "Is a specialised Y"      │
│ Best for         │ Capabilities / roles        │ Type families             │
│ Python tool      │ Protocol (typing) or        │ ABC + @abstractmethod     │
│                  │ ABC with all @abstractmethod│ with concrete methods     │
│ Examples         │ Serializable, Comparable,   │ Animal, Shape, Report,    │
│                  │ Drawable, Hashable          │ BaseHTTPHandler           │
└──────────────────┴────────────────────────────┴───────────────────────────┘
```

---

## Practical Examples

### When to Use an Interface

```
A payment system has different payment methods:
CreditCard, PayPal, Crypto, BankTransfer.

They share NO state and NO common behaviour.
They simply all need to honour: charge(amount), refund(amount).

→ Use an interface (Protocol / ABC with all abstract methods).

  <<interface>>
  PaymentMethod
  + charge(amount: float) → Receipt
  + refund(amount: float) → bool
```

### When to Use an Abstract Class

```
A reporting system generates PDF, CSV, and Excel reports.
All reports share: title, creation date, get_metadata().
Each format implements its own: generate(), format_header().

→ Use an abstract class.

  <<abstract>>
  BaseReport
  + __init__(title)      [concrete — shared]
  + get_metadata()       [concrete — shared]
  + generate()           [abstract — each format decides]
  + format_header()      [abstract — each format decides]
```

---

## Python Tools

```
INTERFACE-STYLE (all abstract):
  from abc import ABC, abstractmethod

  class Drawable(ABC):
      @abstractmethod
      def draw(self) -> None: ...

      @abstractmethod
      def resize(self, factor: float) -> None: ...

  # OR use typing.Protocol for structural subtyping (duck typing):
  from typing import Protocol

  class Drawable(Protocol):
      def draw(self) -> None: ...
      def resize(self, factor: float) -> None: ...

ABSTRACT CLASS (mixed concrete + abstract):
  from abc import ABC, abstractmethod

  class BaseReport(ABC):
      def __init__(self, title: str):
          self._title = title                      # concrete shared state

      def get_metadata(self) -> dict:              # concrete shared method
          return {"title": self._title}

      @abstractmethod
      def generate(self) -> str: ...              # subclass must implement

      @abstractmethod
      def format_header(self) -> str: ...         # subclass must implement
```
