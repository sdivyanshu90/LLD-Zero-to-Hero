# State Pattern

> **The one-line idea:** Allow an object to **alter its behaviour when its internal state changes** — the object will appear to change its class.

---

## Real-World Analogy — Traffic Light

```
A traffic light has ONE physical device, but THREE states:

  ┌──────────┐      timer      ┌──────────┐      timer      ┌──────────┐
  │  GREEN   │ ─────────────► │  YELLOW  │ ─────────────►  │   RED    │
  │          │                 │          │                  │          │
  │ go()     │                 │ go()     │                  │ go()     │
  │ = drive  │                 │ = slow   │                  │ = stop   │
  └──────────┘                 └──────────┘                  └──────────┘
       ▲                                                           │
       └───────────────────────────────────────────────────────────┘
                                  timer

The SAME traffic_light.go() call produces different behaviour
depending on which state the light is currently in.
```

---

## Without State Pattern — Fragile Switch

```
class TrafficLight:
    def go(self):
        if self._state == "green":
            print("Drive through")
        elif self._state == "yellow":
            print("Slow down")
        elif self._state == "red":
            print("Stop")
    # Adding a new state (flashing amber) → MODIFY this class.
    # Adding a new action (honk()) → MORE if/elif blocks.
```

---

## Structure

```
              ┌─────────────────────────────────────────────────┐
              │                   Context                        │
              │           TrafficLight                           │
              │  - _state: TrafficLightState                     │
              │                                                  │
              │  + set_state(state: TrafficLightState) → None    │
              │  + go() → None                                   │
              │    → self._state.go(self)                        │
              │  + timer_expired() → None                        │
              │    → self._state.timer_expired(self)             │
              └─────────────────────────────────────────────────┘
                                    │ has a
                                    ▼
              ┌─────────────────────────────────────────────────┐
              │              <<abstract>>                        │
              │           TrafficLightState                      │
              │  + go(context: TrafficLight) → None              │
              │  + timer_expired(context: TrafficLight) → None   │
              └─────────────────────────────────────────────────┘
                                    ▲
              ┌─────────────────────┼─────────────────────┐
              │                     │                      │
  ┌──────────────────────┐  ┌──────────────────┐  ┌──────────────────┐
  │       GreenState     │  │   YellowState    │  │    RedState      │
  │  go(ctx)             │  │  go(ctx)         │  │  go(ctx)         │
  │  → "Drive through"   │  │  → "Slow down"   │  │  → "Stop"        │
  │  timer_expired(ctx)  │  │  timer_expired() │  │  timer_expired() │
  │  → ctx.set_state(    │  │  → ctx.set_state │  │  → ctx.set_state │
  │      YellowState())  │  │      (RedState())│  │      (GreenState)│
  └──────────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## State Transition Walkthrough

```
light = TrafficLight(initial_state=GreenState())

light.go()            → "Drive through"
light.timer_expired() → switches to YellowState

light.go()            → "Slow down"
light.timer_expired() → switches to RedState

light.go()            → "Stop"
light.timer_expired() → switches back to GreenState

Each state object controls:
  1. What to DO in that state (go, stop, etc.)
  2. What to TRANSITION TO on each event (timer_expired, etc.)
```

---

## State vs. Strategy — Key Difference

```
┌────────────────────────────────────────────────────────────────────┐
│                  STATE                       STRATEGY              │
├────────────────────────────────────────────────────────────────────┤
│ Purpose       │ Object changes behaviour   │ Inject interchangeable│
│               │ as internal state evolves  │ algorithm at runtime  │
│ Transitions   │ States know about and      │ Strategies are        │
│               │ trigger each other         │ unaware of each other │
│ Lifecycle     │ State changes are          │ Strategy set once     │
│               │ automatic (internal logic) │ by external code      │
│ Analogy       │ Traffic light phases       │ Navigation routing    │
│               │ (self-transitions)         │ (user selects method) │
└────────────────────────────────────────────────────────────────────┘
```

---

## When to Use / Avoid

```
USE when:
  ✓  An object's behaviour depends on its state and must change at runtime
  ✓  You have large if/elif blocks that branch on a state variable
  ✓  Transitions between states need to be explicit and documented

AVOID when:
  ✗  You have only 2 states — a simple boolean flag is cleaner
  ✗  State transitions never happen (the state is fixed after construction)
```

---

## State Checklist

```
  □  Does the Context delegate all state-specific behaviour to the State object?
     No if/elif in Context → delegating correctly.

  □  Does each State know which state to transition to on each event?
     If transitions live in Context → move them to the State classes.

  □  Are all states represented as objects, not string/int constants?
     String constants = fragile; objects = type-safe and extensible.

  □  Adding a new state only requires a new State class, not editing
     existing State classes or the Context?
     If yes → OCP is satisfied.
```
