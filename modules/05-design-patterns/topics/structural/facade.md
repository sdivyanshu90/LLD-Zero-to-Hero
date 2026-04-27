# Facade Pattern

> **The one-line idea:** Provide a **single, simplified interface** to a complex subsystem — hide the complexity behind one friendly front door.

---

## Real-World Analogy — Hotel Concierge

```
You want a great evening out. You tell the concierge:
  "Set up a dinner for two at 7 PM, then theatre tickets, then a taxi home."

The concierge coordinates:
  → calls the restaurant
  → calls the theatre box office
  → calls the taxi company
  → confirms all timings fit

You made ONE request. The concierge handled TEN calls.
You never dialled a single number yourself.
```

---

## The Problem Without Facade

```
To watch a movie, the client must orchestrate 4 systems:

  projector.on()
  projector.set_input("BluRay")
  amp.on()
  amp.set_volume(8)
  amp.set_surround_mode("Dolby")
  bluray.on()
  bluray.load_disc("Inception")
  bluray.play()
  lights.dim(20)
  screen.lower()

10 steps, 4 different objects, order matters.
Client code is tightly coupled to every subsystem.
```

---

## The Fix — HomeTheatreFacade

```
           ┌──────────────────────────────────────────────────────────┐
           │                  HomeTheatreFacade                       │
           │                                                          │
           │  - _projector: Projector                                 │
           │  - _amp: Amplifier                                        │
           │  - _bluray: BluRayPlayer                                  │
           │  - _lights: SmartLights                                   │
           │                                                          │
           │  + watch_movie(title: str) → None                        │
           │  + end_movie() → None                                    │
           └──────────────────────────────────────────────────────────┘
               │          │          │          │
               ▼          ▼          ▼          ▼
          Projector   Amplifier  BluRayPlayer  SmartLights
          (complex)   (complex)   (complex)    (complex)

Client code:
  facade = HomeTheatreFacade(projector, amp, bluray, lights)
  facade.watch_movie("Inception")   # one call, all complexity hidden
  facade.end_movie()
```

---

## watch_movie() internals

```
  watch_movie("Inception"):
    lights.dim(20)
    projector.on()
    projector.set_input("BluRay")
    amp.on()
    amp.set_volume(8)
    amp.set_surround_mode("Dolby")
    bluray.on()
    bluray.load_disc("Inception")
    bluray.play()

  end_movie():
    bluray.stop()
    bluray.off()
    amp.off()
    projector.off()
    lights.set_brightness(100)

Subsystems still exist and are accessible directly if needed.
Facade does NOT lock them away — it just simplifies the common path.
```

---

## Facade vs. Adapter

```
┌──────────────────────────────────────────────────────────────────────┐
│                   FACADE                      ADAPTER                │
├──────────────────────────────────────────────────────────────────────┤
│ Problem solved  │ Too complex              │ Incompatible interfaces │
│ Interfaces      │ New simplified interface │ Matches existing target  │
│                 │ over complex subsystem   │ interface exactly        │
│ Number of       │ Many subsystem classes   │ Typically one adaptee    │
│ classes wrapped │                          │                          │
│ Analogy         │ Hotel concierge          │ Travel plug adapter      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## When to Use / Avoid

```
USE when:
  ✓  A subsystem is complex and clients only need a subset of its functionality
  ✓  You want to layer a system and only expose the higher layer's interface
  ✓  You want to decouple client code from multiple subsystem classes

AVOID when:
  ✗  The "simplification" is so thin it adds no real value
  ✗  Clients regularly need direct access to subsystem features
     (consider just leaving subsystems accessible directly)
```

---

## Facade Checklist

```
  □  Does the facade expose a small, simple interface (2-5 methods)?
     If 15+ methods → the facade might be a God class itself.

  □  Does the facade coordinate subsystems but NOT contain business logic?
     If it does → extract the logic to a service or domain object.

  □  Can clients still access the subsystems directly when needed?
     If not → you've hidden necessary functionality.
```
