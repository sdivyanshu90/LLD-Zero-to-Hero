# Encapsulation

> **The one-line idea:** Bundle data and the methods that operate on it into one unit, and **control who can touch the data**.

---

## Real-World Analogy — The ATM Machine

```
                   ┌─────────────────────────────┐
  USER SEES:       │          ATM                │
                   │                             │
  [Card Slot]      │   ┌─────────────────────┐   │
  [PIN Pad]   ───► │   │  HIDDEN INTERNALS   │   │
  [Screen]         │   │  - vault mechanism  │   │
  [Cash Slot]      │   │  - bank connection  │   │
                   │   │  - cash counter     │   │
                   │   │  - audit log        │   │
                   │   └─────────────────────┘   │
                   └─────────────────────────────┘
                           ▲
                    You interact ONLY through
                    the public interface.
                    The internals are protected.
```

You can't reach into the ATM and grab cash directly. The machine *controls* how you interact with its internal state.

---

## The Problem Without Encapsulation

```
Without encapsulation:

  BankAccount
  ├── balance = 1000      ← PUBLIC: anyone can write account.balance = -99999
  └── owner = "Alice"     ← PUBLIC: anyone can change ownership

  External code:
    account.balance = -99999   ← No validation! Invariant broken.
```

```
With encapsulation:

  BankAccount
  ├── _balance = 1000     ← PRIVATE: hidden from outside
  ├── _owner = "Alice"    ← PRIVATE: hidden from outside
  │
  ├── deposit(amount)     ← PUBLIC gateway — validates amount > 0
  ├── withdraw(amount)    ← PUBLIC gateway — validates sufficient funds
  └── get_balance()       ← PUBLIC read-only access

  External code:
    account.withdraw(-500)  → raises ValueError: "Amount must be positive"
    account._balance = 0    → convention says "don't do this"
```

---

## The Three Levels of Access

```
┌──────────────────────────────────────────────────────────┐
│               ACCESS LEVELS (Python conventions)         │
│                                                          │
│  PUBLIC      name          Accessible by everyone        │
│  ─────────────────────────────────────────────────────   │
│  PROTECTED   _name         "Please don't touch" signal   │
│              (single underscore)   — convention only     │
│  ─────────────────────────────────────────────────────   │
│  PRIVATE     __name        Name-mangled by Python →      │
│              (double underscore)  _ClassName__name       │
│              Hard(er) to access from outside the class   │
└──────────────────────────────────────────────────────────┘
```

---

## The Invariant Protection Pattern

An **invariant** is a rule that must *always* be true about an object's state.

```
Invariant for BankAccount: balance must always be >= 0

Without encapsulation → invariant can be violated at any time.
With encapsulation    → invariant is enforced at every write point.

┌─────────────────────────────────────────────────────────┐
│               BankAccount (encapsulated)                │
│                                                         │
│  STATE (private):                                       │
│    _balance: float       invariant: _balance >= 0       │
│                                                         │
│  ENTRY POINTS (public):                                 │
│    deposit(amount)   → validates amount > 0             │
│    withdraw(amount)  → validates amount > 0             │
│                         AND amount <= _balance          │
│    balance (property) → read-only; no setter            │
└─────────────────────────────────────────────────────────┘
```

---

## Encapsulation ≠ Just Adding Getters/Setters

> Bad encapsulation: hiding a field behind a getter and setter that do **nothing**.  
> Good encapsulation: hiding a field behind methods that **enforce rules**.

```
BAD — just renaming access, no protection:
  def set_age(self, age):
      self._age = age          # Anyone can still set age = -100

GOOD — enforcing the invariant:
  def set_age(self, age):
      if age < 0 or age > 150:
          raise ValueError("Age out of realistic range")
      self._age = age
```

---

## Encapsulation Checklist

```
For every class you write, ask:

  □  Is every field that callers shouldn't write to hidden?
     (_field or __field, exposed via read-only @property if needed)

  □  Does every setter/method validate its input before storing it?
     (No invariant-breaking state should ever be stored)

  □  Is the internal representation free to change?
     (Can you refactor _balance from float to Decimal without
      callers knowing? If yes → well-encapsulated)

  □  Can you test the class without knowing its internals?
     (Good encapsulation means testing through the public interface)
```
