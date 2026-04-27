# UML Notation

> **The one-line idea:** UML is a universal visual language for expressing *who knows about whom* and *how strongly* they are coupled — without writing a single line of code.

---

## Relationship Glossary

```
RELATIONSHIP        ARROW STYLE          MEANING
──────────────────────────────────────────────────────────────────────────
Inheritance         ───────────────►     IS-A (solid line, hollow head)
                    (solid, open triangle)

Realization         ···················► IMPLEMENTS (dotted, hollow head)
                    (dotted, open triangle)

Composition         ◆──────────────      OWNS (filled diamond on owner)

Aggregation         ◇──────────────      USES (hollow diamond on container)

Association         ───────────────►     KNOWS-ABOUT (solid, open arrow)

Dependency          ···················► TEMPORARILY-USES (dotted, open arrow)
                    (dotted, open arrow)
```

### Memory Aid

```
  Solid line  = permanent / structural relationship
  Dotted line = temporary / weaker relationship

  Triangle head = "type relationship"  (inheritance / realization)
  Arrow head    = "direction of knowledge"
  Diamond       = "whole-part"  (filled = owns, hollow = uses)
```

---

## Class Box Anatomy

```
┌──────────────────────────────────────────────┐
│               ClassName                       │  ← name (bold, centered)
├──────────────────────────────────────────────┤
│  - _private_field: str                        │
│  # _protected_field: int                      │  ← attributes
│  + public_field: float                        │
├──────────────────────────────────────────────┤
│  + public_method(arg: str) → bool             │
│  # _protected_method() → None                 │  ← methods
│  - __private_method() → None                  │
└──────────────────────────────────────────────┘

VISIBILITY SYMBOLS:
  + (plus)     → public    — accessible from anywhere
  - (minus)    → private   — accessible only within the class
  # (hash)     → protected — accessible within class and subclasses
  ~ (tilde)    → package   — accessible within same package (Java/C#)
```

---

## Multiplicity Notation

```
NOTATION    MEANING
──────────────────────────────────
1           Exactly one
0..1        Zero or one (optional)
*  or 0..*  Zero or more
1..*        One or more
2..5        Between 2 and 5
3           Exactly 3

EXAMPLES:

  Person ─────────────── Address
          1         0..*
  One person has zero-or-more addresses.

  Order ◆──────────────── OrderItem
         1         1..*
  One order contains one-or-more order items.

  Student ◇──────────────── Course
           0..*       0..*
  A student can be in zero-or-more courses; a course has zero-or-more students.
```

---

## Full Library System Example

Step-by-step diagram construction:

**Step 1 — Identify entities:**
- Library, Book, Member, Loan

**Step 2 — Establish relationships:**
- Library OWNS Books (Composition — books are part of library)
- Library has Members (Aggregation — members exist independently)
- Member borrows Books via Loan (Association)

**Step 3 — Add multiplicities:**
- One Library has many Books (1 : 1..*)
- One Library has many Members (1 : 0..*)
- One Member has many Loans (1 : 0..*)
- One Book can be in many Loans over time (1 : 0..*)

**Step 4 — Draw the diagram:**

```
┌───────────────────┐
│    Library         │
├───────────────────┤
│  + name: str       │
│  + address: str    │
├───────────────────┤
│  + add_book()      │
│  + register()      │
└───────────────────┘
        │ ◆ 1
        │
        │ 1..*
┌────────────────┐           ┌──────────────────┐
│     Book        │           │     Member        │
├────────────────┤           ├──────────────────┤
│  + isbn: str    │     ◇─── │  + member_id: str │
│  + title: str   │  0..*1   │  + name: str      │
│  + author: str  │           ├──────────────────┤
├────────────────┤           │  + borrow()       │
│  + is_available │           │  + return_book()  │
└────────────────┘           └──────────────────┘
        │ 1                          │ 1
        │                            │
        │ 0..*                       │ 0..*
        └──────────┬─────────────────┘
                   │
          ┌────────────────┐
          │      Loan       │
          ├────────────────┤
          │ + loan_id: str  │
          │ + borrow_date   │
          │ + due_date      │
          ├────────────────┤
          │ + is_overdue()  │
          └────────────────┘
```

---

## Red Flags Checklist

```
  □  Everything connects to one "god" class?
     → SRP violation. Split that class.

  □  Composition used where aggregation is correct (child can live independently)?
     → Wrong lifetime coupling; switch to aggregation.

  □  No multiplicities on associations?
     → Diagram is ambiguous; add them.

  □  Circular dependency between classes at the same level?
     → Smell; introduce an interface or inversion.

  □  Arrow direction unclear (who knows about whom)?
     → Add arrowheads to all associations.

  □  Class box has 20+ methods?
     → Likely too many responsibilities; refactor.
```
