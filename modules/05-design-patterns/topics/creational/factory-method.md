# Factory Method Pattern

> **The one-line idea:** Define an interface for creating an object, but let subclasses (or a dedicated factory) decide which class to instantiate. The caller never uses `new` / `ClassName()` directly.

---

## Real-World Analogy — Pizza Counter

```
You walk up to a pizza counter and say: "One pizza, please."
You don't specify what oven to use, which dough recipe to follow,
or which supplier to source the cheese from.

The counter (the factory) knows all those details.
You receive a pizza — a finished product — without seeing any internals.

Changing the supplier? The counter changes, not you.
Adding a vegan pizza? The counter adds it, your order stays the same.
```

---

## Structure — Abstract Factory Method

```
                  ┌──────────────────────────────────────┐
                  │         <<abstract>>                  │
                  │     NotificationFactory               │
                  │                                       │
                  │  + create_notification()              │
                  │    → Notification  [abstract]         │
                  │                                       │
                  │  + send(message: str)  [concrete]     │
                  │    n = create_notification()          │
                  │    n.notify(message)                  │
                  └──────────────────────────────────────┘
                                    ▲
               ┌────────────────────┼──────────────────────┐
               │                    │                       │
  ┌──────────────────────┐  ┌──────────────────┐  ┌───────────────────┐
  │  EmailNotification   │  │  SMSNotification  │  │ PushNotification  │
  │  Factory             │  │  Factory          │  │ Factory           │
  │  create_notification │  │  create_notif.    │  │ create_notif.     │
  │  → EmailNotification │  │  → SMSNotif.      │  │ → PushNotif.      │
  └──────────────────────┘  └──────────────────┘  └───────────────────┘

                 ┌──────────────────────────────────────┐
                 │         <<interface>>                 │
                 │          Notification                 │
                 │  + notify(message: str) → None        │
                 └──────────────────────────────────────┘
                               ▲
          ┌────────────────────┼─────────────────────┐
          │                    │                      │
   ┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐
   │EmailNotif.   │  │  SMSNotif.       │  │  PushNotif.      │
   │notify()      │  │  notify()        │  │  notify()        │
   └──────────────┘  └──────────────────┘  └──────────────────┘
```

---

## Simple Factory Variant (not a GoF pattern, but common)

```
When you don't need subclassing of the factory itself:

class NotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        if channel == "email":
            return EmailNotification()
        elif channel == "sms":
            return SMSNotification()
        elif channel == "push":
            return PushNotification()
        raise ValueError(f"Unknown channel: {channel}")

Caller:
    notif = NotificationFactory.create("email")
    notif.notify("Your order has shipped.")

Downside: still has an if/elif block (violates OCP).
```

---

## When to Use

```
USE when:
  ✓  The exact type of object to create isn't known until runtime
  ✓  You want to decouple the caller from concrete product classes
  ✓  You anticipate adding new product types (OCP compliance)

AVOID when:
  ✗  There is only one product type (no variation needed)
  ✗  The overhead of an extra abstraction layer is not justified
```

---

## Factory Method Checklist

```
  □  Does the caller ever reference a concrete class by name?
     If yes → introduce a factory to hide the construction.

  □  Is object creation logic duplicated across multiple places?
     If yes → centralise it in a factory.

  □  Will new product types be added regularly?
     If yes → prefer abstract factory method over simple if/elif factory.
```
