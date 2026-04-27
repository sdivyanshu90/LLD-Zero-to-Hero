# Adapter Pattern

> **The one-line idea:** Convert the interface of a class into the interface a client expects — act as a **translator** between two incompatible interfaces without changing either.

---

## Real-World Analogy — Travel Power Adapter

```
Your laptop plug (client):      expects a 3-pin round socket
The hotel wall socket (adaptee): provides 2-pin flat socket

You cannot modify your laptop plug.
You cannot modify the wall socket.

The travel adapter (Adapter):
  - accepts your 3-pin round plug
  - plugs into the 2-pin flat socket
  - translates between the two

Both sides remain unchanged. The adapter bridges the gap.
```

---

## Structure

```
                  ┌──────────────────────────────┐
                  │       <<interface>>           │
                  │          Logger               │     ← what the client expects
                  │                               │
                  │  + log(level: str,            │
                  │         message: str) → None  │
                  └──────────────────────────────┘
                               ▲
              ┌────────────────┴────────────────┐
              │                                 │
   ┌──────────────────────┐     ┌─────────────────────────────────────┐
   │    ConsoleLogger     │     │         AuditLoggerAdapter           │
   │  log(level, message) │     │  - _lib: ThirdPartyAuditLibrary      │
   │  → prints to stdout  │     │  + log(level, message)  [adapts]     │
   └──────────────────────┘     │    → translates to _lib.write_audit()│
                                └─────────────────────────────────────┘
                                                │ uses
                                                ▼
                                ┌──────────────────────────────┐
                                │   ThirdPartyAuditLibrary      │
                                │   (incompatible interface)    │
                                │  + write_audit(entry: dict)   │
                                │  + set_severity(n: int)       │
                                └──────────────────────────────┘
```

---

## How the Translation Works

```
Client calls:
  logger.log("ERROR", "Payment failed")

AuditLoggerAdapter translates:
  def log(self, level: str, message: str) → None:
      severity = {"DEBUG": 1, "INFO": 2, "WARNING": 3, "ERROR": 4}[level]
      self._lib.set_severity(severity)
      self._lib.write_audit({"message": message, "timestamp": now()})

ThirdPartyAuditLibrary receives:
  set_severity(4)
  write_audit({"message": "Payment failed", "timestamp": "2024-01-15T10:30:00"})
```

---

## Adapter vs. Facade

```
┌──────────────────────────────────────────────────────────────────────┐
│                   ADAPTER                     FACADE                 │
├──────────────────────────────────────────────────────────────────────┤
│ Purpose       │ Interface translation    │ Simplified interface       │
│ Interfaces    │ TWO existing interfaces  │ One new simplified one     │
│               │ must become compatible   │ over a complex subsystem   │
│ What changes  │ Nothing in either side   │ Nothing in subsystem       │
│ Motivation    │ Incompatibility problem  │ Complexity problem         │
│ Analogy       │ Travel plug adapter      │ Hotel concierge service    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## When to Use / Avoid

```
USE when:
  ✓  You want to use an existing class but its interface doesn't match
  ✓  Integrating a third-party library with your internal interface
  ✓  Making legacy code work with a new interface

AVOID when:
  ✗  You can change one of the interfaces directly (no need for indirection)
  ✗  The "incompatibility" is just naming — a thin wrapper adds no value
```

---

## Adapter Checklist

```
  □  Did you identify the Target interface (what the client expects)?
  □  Did you identify the Adaptee (the incompatible existing class)?
  □  Does the Adapter implement the Target interface?
  □  Does the Adapter delegate to the Adaptee (composition, not inheritance)?
  □  Does the client only see the Target interface (never the Adaptee)?
```
