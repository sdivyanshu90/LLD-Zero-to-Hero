# Abstraction

> **The one-line idea:** Show only what the caller needs; **hide how it works inside**.

---

## Real-World Analogy — Driving a Car

```
┌──────────────────────────────────────────────────────────┐
│                     CAR INTERFACE                        │
│                                                          │
│   [Steering wheel]  [Accelerator]  [Brake]  [Gear]       │
│                                                          │
│   These are ALL you need to drive.                       │
│                                                          │
│   ┌──────────────────────────────────────────────────┐   │
│   │              HIDDEN COMPLEXITY                   │   │
│   │  - Fuel injection timing                         │   │
│   │  - Valve timing                                  │   │
│   │  - ABS algorithm                                 │   │
│   │  - Power steering hydraulics                     │   │
│   │  - Transmission gear selection logic             │   │
│   └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

The complexity underneath can change completely (petrol → electric), but you still just press the accelerator. The **interface** is stable; the **implementation** can vary.

---

## Abstraction vs. Encapsulation — The Common Confusion

These are related but distinct:

```
┌────────────────────┬──────────────────────────────────────────────┐
│                    │                                              │
│  ENCAPSULATION     │  HOW you protect data                        │
│                    │  → bundling + access control                 │
│                    │  → hiding the STATE                          │
│                    │                                              │
├────────────────────┼──────────────────────────────────────────────┤
│                    │                                              │
│  ABSTRACTION       │  WHAT you expose to the outside world        │
│                    │  → defining a clean interface/contract       │
│                    │  → hiding the IMPLEMENTATION                 │
│                    │                                              │
└────────────────────┴──────────────────────────────────────────────┘

Encapsulation is the TOOL.
Abstraction is the GOAL.
```

---

## Abstraction in Code — The Contract Model

```
             ┌───────────────────────────────┐
             │       MessageSender           │  ← ABSTRACT INTERFACE
             │  (what you can do with it)    │     (the "what")
             │                               │
             │  + send(recipient, message)   │
             │  + get_status() -> Status     │
             └───────────────────────────────┘
                          ▲
            ┌─────────────┴──────────────┐
            │                            │
 ┌──────────────────┐        ┌───────────────────────┐
 │   EmailSender    │        │     SMSSender          │
 │  (the "how")     │        │    (the "how")         │
 │                  │        │                        │
 │  - smtp_client   │        │  - twilio_client       │
 │  - auth_token    │        │  - phone_number_lookup │
 │                  │        │                        │
 │  send(...)       │        │  send(...)             │
 └──────────────────┘        └───────────────────────┘
```

The caller only knows about `MessageSender`. It calls `send()` without knowing or caring whether email or SMS is used under the hood.

---

## Levels of Abstraction

```
HIGH ABSTRACTION
  │   "Send the user a notification"
  │      │
  │      ▼
  │   NotificationService.notify(user, message)
  │      │
  │      ▼
  │   MessageSender.send(address, content)
  │      │
  │      ▼
  │   SMTPClient.connect(host, port)
  │      │
  │      ▼
  │   socket.send(bytes)
  │
LOW ABSTRACTION
```

> **Good design:** each layer only talks to the layer directly below it. High-level code never reaches past its immediate abstraction.

---

## Why Abstraction Matters for LLD

```
Without abstraction:
  OrderProcessor directly creates a MySQLDatabase object.
  To switch to PostgreSQL → must rewrite OrderProcessor.

With abstraction:
  OrderProcessor depends on a Database interface.
  MySQLDatabase and PostgresDatabase both implement Database.
  To switch → swap the concrete class; OrderProcessor is untouched.

  ┌────────────────┐        ┌──────────────────┐
  │ OrderProcessor │───────►│   <<interface>>  │
  └────────────────┘        │   Database       │
                            │  + query(sql)    │
                            │  + execute(sql)  │
                            └──────────────────┘
                                     ▲
                        ┌────────────┴────────────┐
                        │                         │
               ┌─────────────────┐    ┌──────────────────┐
               │  MySQLDatabase  │    │ PostgresDatabase  │
               └─────────────────┘    └──────────────────┘
```

---

## Abstraction Checklist

```
For every interface or abstract class, ask:

  □  Does the caller need to know HOW this is implemented?
     If no → abstract it behind an interface.

  □  Could I swap the implementation without the caller noticing?
     If yes → abstraction is working correctly.

  □  Is the abstraction at the right level?
     Too low: exposes implementation details.
     Too high: forces callers to do too much themselves.

  □  Does the name describe WHAT it does, not HOW?
     Good: MessageSender, PaymentProcessor, OrderRepository
     Bad:  SMTPEmailViaGmailAPI, MySQLOrderWriter
```
