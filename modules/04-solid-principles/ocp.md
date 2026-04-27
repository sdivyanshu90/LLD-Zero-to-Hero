# Open/Closed Principle (OCP)

> **The one-line idea:** Classes should be **open for extension** but **closed for modification** — add new behaviour by writing new code, not by editing existing code.

---

## Real-World Analogy — USB Ports

```
Your laptop has USB ports (closed for modification — you can't change the laptop):
  ┌───────────────────────────────────────────┐
  │                  LAPTOP                    │
  │   [USB Port] [USB Port] [USB Port]         │
  └───────────────────────────────────────────┘

But you can extend it by plugging in new devices (open for extension):
  → Plug in a mouse        (new behaviour, no laptop modification)
  → Plug in a USB keyboard (new behaviour, no laptop modification)
  → Plug in a USB speaker  (new behaviour, no laptop modification)

The contract (USB interface) stays stable.
New capabilities come from new plug-in devices.
```

---

## The Violation — if/elif Chain

```
class DiscountCalculator:
    def calculate(self, order, customer_type: str) -> float:
        if customer_type == "regular":
            return order.total * 0.0
        elif customer_type == "premium":
            return order.total * 0.10
        elif customer_type == "vip":
            return order.total * 0.20
        # Add "employee" discount? → MODIFY THIS FUNCTION → risk breaking existing cases
```

**Why this violates OCP:**

```
                              DiscountCalculator
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                     │
         "regular" path       "premium" path        "vip" path
                                     │
                              ┌──────▼──────┐
                              │ ADD "employee"?│
                              │ EDIT the method │  ← closed for modification VIOLATED
                              └─────────────┘
```

Every new customer type forces you to crack open a method that already works.

---

## The Fix — Polymorphic Extension

```
                        ┌──────────────────────┐
                        │  <<interface>>        │
                        │  DiscountStrategy     │
                        │                       │
                        │  + calculate(order)   │
                        │    → float            │
                        └──────────────────────┘
                                   ▲
            ┌──────────────────────┼─────────────────────────────┐
            │                      │                   │         │
  ┌─────────────────┐  ┌───────────────────┐  ┌──────────────────┐
  │ NoDiscount      │  │ PremiumDiscount    │  │  VIPDiscount     │
  │ calculate()→0%  │  │ calculate()→10%   │  │ calculate()→20%  │
  └─────────────────┘  └───────────────────┘  └──────────────────┘
                                                        |
                                              Add EmployeeDiscount?
                                              → Write NEW class    ← open for extension
                                              → Touch NOTHING else ← closed for modification

class DiscountCalculator:
    def calculate(self, order, strategy: DiscountStrategy) -> float:
        return strategy.calculate(order)   # never changes regardless of new strategies
```

---

## Two Mechanisms for OCP

```
MECHANISM 1 — Polymorphism (most common):
  Define an abstract interface.
  New behaviour = new class implementing the interface.
  Caller holds a reference to the interface, not the concrete class.

MECHANISM 2 — Composition / Injection:
  Pass collaborators into the class (constructor / method injection).
  Swap behaviour without modifying the class.
  
  class NotificationService:
      def __init__(self, sender: MessageSender):  ← injected
          self._sender = sender

      def notify(self, message: str):
          self._sender.send(message)     ← same code, different sender per use
```

---

## When to Apply OCP

```
Apply OCP when you see these signals:

  ✓  You predict this area will need new variants (e.g., new payment types,
     new export formats, new discount rules)

  ✓  The if/elif/switch block grows every sprint

  ✓  Multiple teams/modules share the same class that keeps changing

Do NOT gold-plate with OCP prematurely:

  ✗  The logic will never have more than one variant
  ✗  The "extension points" are purely speculative (YAGNI)
  ✗  Adding an interface just to satisfy a principle adds complexity with
     no real benefit
```

---

## OCP Checklist

```
  □  Are you about to add a new if/elif branch to existing working code?
     Consider introducing an interface + new subclass instead.

  □  Can you add the new behaviour by writing a new file only?
     If yes → your design already honours OCP.

  □  Does your caller depend on a concrete class by name?
     If yes → depend on an abstraction instead to unlock OCP.

  □  Is the class under frequent modification by different people?
     If yes → it's not closed. Abstract the variation points.
```
