# Observer Pattern

> **The one-line idea:** Define a **one-to-many dependency** so that when one object changes state, all its dependents are notified and updated automatically.

---

## Real-World Analogy — YouTube Subscriptions

```
┌─────────────────────────────────────────────────────────────┐
│                   YouTube Channel                           │
│                   (Subject / Publisher)                     │
│                                                             │
│   On new video upload:                                      │
│     → Notify all subscribers                                │
└─────────────────────────────────────────────────────────────┘
              │
     ┌────────┼────────┐
     │        │        │
     ▼        ▼        ▼
  User A   User B   User C
 (gets   (gets    (gets
  notif.) notif.)  notif.)

User A unsubscribes → future uploads no longer notify User A.
User D subscribes → future uploads will include User D.
The channel doesn't need to know who exactly the subscribers are.
```

---

## Structure

```
               ┌──────────────────────────────────────────┐
               │           <<interface>>                   │
               │              Subject                      │
               │  + attach(observer: Observer) → None      │
               │  + detach(observer: Observer) → None      │
               │  + notify() → None                        │
               └──────────────────────────────────────────┘
                              ▲
              ┌───────────────┘
              │
   ┌───────────────────────────────────────────────────────┐
   │                   StockMarket                         │
   │  - _observers: list[Observer]                         │
   │  - _price: float                                      │
   │                                                       │
   │  + attach(observer) → None                            │
   │  + detach(observer) → None                            │
   │  + notify() → None                                    │
   │    for o in _observers: o.update(self)                │
   │  + set_price(price: float) → None  ← triggers notify  │
   └───────────────────────────────────────────────────────┘

               ┌──────────────────────────────────────────┐
               │           <<interface>>                   │
               │              Observer                     │
               │  + update(subject: Subject) → None        │
               └──────────────────────────────────────────┘
                              ▲
              ┌───────────────┼───────────────┐
              │               │               │
   ┌──────────────────┐  ┌──────────────┐  ┌───────────────┐
   │  EmailAlert      │  │ MobileAlert  │  │  Dashboard    │
   │  update(subject) │  │ update(sub.) │  │ update(sub.)  │
   │  → send email    │  │ → push notif.│  │ → refresh UI  │
   └──────────────────┘  └──────────────┘  └───────────────┘
```

---

## Event Flow Diagram

```
Step 1: Observers register
  EmailAlert.attach(stock_market)
  Dashboard.attach(stock_market)

Step 2: Subject state changes
  stock_market.set_price(152.30)
         │
         ▼
Step 3: notify() called internally
  for observer in _observers:
      observer.update(self)
         │
         ├──► EmailAlert.update(stock_market)
         │       → reads stock_market.get_price() → sends email
         │
         └──► Dashboard.update(stock_market)
                 → reads stock_market.get_price() → redraws chart

Step 4: Observer detaches
  email_alert.detach(stock_market)
  (next price change won't reach EmailAlert)
```

---

## Push vs. Pull Model

```
PUSH MODEL — Subject sends data in the notification:
  observer.update(new_price: float)
  + Observer gets data immediately
  - Subject must know what data observers need (tighter coupling)

PULL MODEL — Subject sends reference to itself:
  observer.update(subject: Subject)
  + Observer decides what to read (looser coupling)
  - Observer must know the Subject's interface
  - Python standard preference: pass self as the subject

HYBRID — Send event type + minimal data:
  observer.update(event_type: str, subject: Subject)
  Observers filter by event_type to avoid unnecessary processing.
```

---

## When to Use / Avoid

```
USE when:
  ✓  Changes to one object require updating unknown numbers of others
  ✓  Objects should be able to notify others without assumptions about who they are
  ✓  Loose coupling between publisher and subscriber is a priority

AVOID when:
  ✗  Notification chains become long and hard to trace (cascading updates)
  ✗  Observers modify the subject during update (risk of infinite loops)
```

---

## Observer Checklist

```
  □  Does the Subject hold a list of Observer interface references (not concretes)?
  □  Can observers be attached and detached at runtime?
  □  Does notify() call update() on all attached observers?
  □  Does each observer update itself from the subject without the
     subject knowing observer details?
  □  Are memory leaks prevented? (detach observers when no longer needed,
     especially in long-lived subjects)
```
