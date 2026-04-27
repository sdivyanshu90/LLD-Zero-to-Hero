# Single Responsibility Principle (SRP)

> **The one-line idea:** A class should have **one reason to change** — meaning it should encapsulate only one concern or responsibility.

---

## Real-World Analogy — The Swiss Army Knife Problem

```
SWISS ARMY KNIFE (violates SRP for software):

  ┌──────────────────────────────┐
  │        UserManager           │
  │  ─────────────────────────── │
  │  + create_user()             │
  │  + delete_user()             │  ← User data concern
  │  + update_password()         │
  │  ─────────────────────────── │
  │  + send_welcome_email()      │
  │  + send_reset_email()        │  ← Email/notification concern
  │  ─────────────────────────── │
  │  + save_to_database()        │
  │  + load_from_database()      │  ← Persistence concern
  │  ─────────────────────────── │
  │  + generate_report()         │
  │  + export_to_pdf()           │  ← Reporting concern
  └──────────────────────────────┘

  Four reasons this class will change:
  1. Business rules about users change → modify this class
  2. Email provider changes → modify this class
  3. Database schema changes → modify this class
  4. Report format changes → modify this class
```

**SRP says:** each of those is a separate "axis of change" — they belong in separate classes.

---

## The "Reason to Change" Test

```
For every class, ask: "Who might ask me to change this?"

  ┌──────────────────┐         Reason 1: "The marketing team changed
  │   UserManager    │ ◄────── the email template" — stakeholder: Marketing
  └──────────────────┘
           │
           │◄──────────────── Reason 2: "The DBA changed the schema"
           │                            stakeholder: Database Team
           │
           └◄──────────────── Reason 3: "The product team changed
                                          user validation rules"
                                          stakeholder: Product Team

  Three different stakeholders = three different axes of change.
  A class with multiple stakeholders will be a change magnet.
```

---

## After SRP — Separate by Concern

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  UserService │     │  UserEmailService │     │ UserRepository   │
├──────────────┤     ├──────────────────┤     ├──────────────────┤
│ create()     │     │ send_welcome()   │     │ save()           │
│ delete()     │     │ send_reset()     │     │ find_by_id()     │
│ update_pw()  │     └──────────────────┘     │ delete()         │
└──────────────┘                              └──────────────────┘

    ┌──────────────────┐
    │   UserReporter   │
    ├──────────────────┤
    │ generate()       │
    │ export_to_pdf()  │
    └──────────────────┘

Each class has exactly one reason to change.
```

---

## Common SRP Violation Patterns

### Pattern 1 — God Class

```
  A class that "knows" and "does" everything.
  Symptom: 500+ lines, 30+ methods, 15+ instance variables.
  Fix: extract clusters of related methods into focused classes.
```

### Pattern 2 — Mixed Abstraction Levels

```
  A class mixes high-level policy with low-level implementation.

  VIOLATION:
  class OrderProcessor:
      def process(self, order):
          ...business logic...
          cursor.execute("INSERT INTO orders ...")  ← SQL inside business logic

  FIX:
  class OrderProcessor:
      def process(self, order):
          ...business logic...
          self._repo.save(order)                    ← delegates to repo

  class OrderRepository:
      def save(self, order): ...                    ← owns the SQL
```

### Pattern 3 — Data + Behaviour Mismatch

```
  A data class that also implements its own persistence.

  VIOLATION:
  class Invoice:
      def __init__(self): ...
      def calculate_total(self): ...    ← belongs here (domain logic)
      def save_to_db(self): ...         ← does NOT belong here
      def export_pdf(self): ...         ← does NOT belong here

  FIX:
  class Invoice: calculate_total() only
  class InvoiceRepository: save_to_db()
  class InvoiceExporter: export_pdf()
```

---

## SRP Checklist

```
  □  Can you describe this class's purpose in one sentence without using "and"?
     If you need "and" → likely SRP violation.

  □  How many different stakeholder groups would request changes to this class?
     More than one? → Split by stakeholder concern.

  □  Does the class import from radically different domains
     (e.g., db drivers AND email clients AND PDF libraries)?
     If yes → each import group hints at a separate responsibility.

  □  If you test this class, do you need to mock multiple unrelated systems?
     If yes → the class is doing too much.
```
