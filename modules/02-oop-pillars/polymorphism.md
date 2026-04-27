# Polymorphism

> **The one-line idea:** One interface, many behaviours. The same call can produce different actions depending on the **actual type** of the object at runtime.

---

## Real-World Analogy — Universal Remote

```
┌──────────────────────────────────────────────────────────┐
│                   UNIVERSAL REMOTE                       │
│                                                          │
│   [PLAY] button                                          │
│       │                                                  │
│       ├──► Samsung TV  → plays video                    │
│       ├──► Sony TV     → plays video (different circuit) │
│       ├──► DVD Player  → plays disc                     │
│       └──► Music Box   → plays music                    │
│                                                          │
│   Same interface (PLAY), different behaviour per device. │
└──────────────────────────────────────────────────────────┘
```

---

## Two Flavours of Polymorphism

### Flavour 1 — Overriding (Runtime / Dynamic Polymorphism)

The method to call is determined **at runtime** based on the actual object type.

```
                ┌───────────┐
                │   Shape   │
                │  area()   │  ← defined, but behaviour differs per subclass
                └───────────┘
                      ▲
         ┌────────────┼────────────┐
         │            │            │
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │  Circle  │  │Rectangle │  │ Triangle │
   │  area()  │  │  area()  │  │  area()  │
   │ = π r²   │  │ = w × h  │  │= ½ b × h │
   └──────────┘  └──────────┘  └──────────┘

Code:
  shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]
  for shape in shapes:
      print(shape.area())    # Each calls its OWN area()

Call resolution at runtime:
  shape.area()
       │
       └─► Python checks: what is the actual type of shape?
           Circle?    → call Circle.area()
           Rectangle? → call Rectangle.area()
           Triangle?  → call Triangle.area()
```

---

### Flavour 2 — Overloading (Compile-time / Static Polymorphism)

Same method name, different parameter signatures. **Python does not support this natively** (the last definition wins), but you can emulate it:

```
Native overloading (Java/C++ style) — NOT in Python:
  def process(self, x: int): ...
  def process(self, x: str): ...   ← this REPLACES the above!

Python emulation strategies:

  Strategy A — Default arguments:
    def process(self, x, multiplier=1):
        ...

  Strategy B — isinstance checks (avoid when possible):
    def process(self, x):
        if isinstance(x, int): ...
        elif isinstance(x, str): ...

  Strategy C — functools.singledispatch (clean, preferred):
    @singledispatch
    def process(x):
        raise NotImplementedError

    @process.register(int)
    def _(x): ...

    @process.register(str)
    def _(x): ...
```

---

## The Power of Polymorphism — Open/Closed Principle in Action

```
WITHOUT polymorphism — adding a new shape MODIFIES existing code:

  def total_area(shapes):
      total = 0
      for s in shapes:
          if s.type == "circle":
              total += 3.14 * s.radius ** 2
          elif s.type == "rectangle":
              total += s.width * s.height
          # Add triangle? → MODIFY this function → risk breaking existing cases
      return total

WITH polymorphism — adding a new shape requires ZERO changes here:

  def total_area(shapes):
      return sum(s.area() for s in shapes)
      # New shape type? Just implement area(). This function stays closed.
```

---

## Duck Typing — Python's Natural Polymorphism

Python doesn't require a formal inheritance relationship for polymorphism:

```
"If it walks like a duck and quacks like a duck, it's a duck."

class Dog:
    def speak(self): return "Woof"

class Cat:
    def speak(self): return "Meow"

class Robot:
    def speak(self): return "Beep boop"

def make_noise(things):
    for thing in things:
        print(thing.speak())   # No shared base class needed!

make_noise([Dog(), Cat(), Robot()])   # Works perfectly
```

This is polymorphism through **interface compatibility**, not inheritance.

---

## Polymorphism Decision Tree

```
I want different behaviour based on object type
              │
              ▼
  Is there a genuine IS-A relationship?
        │                 │
       YES               NO
        │                 │
        ▼                 ▼
  Use inheritance    Use duck typing or
  + method override  composition + protocol
        │
        ▼
  Is the behaviour variation known at design time?
        │                 │
       YES               NO
        │                 │
        ▼                 ▼
  Override in       Use Strategy pattern
  subclasses        (see Module 5)
```

---

## Polymorphism Checklist

```
  □  Can I treat all variants uniformly through one interface?
     If no → your abstraction is leaking.

  □  Does adding a new variant require modifying existing call sites?
     If yes → the design is not polymorphic enough.

  □  Am I using isinstance() to branch on type?
     If yes → that is a smell; consider polymorphism instead.

  □  Are all variants truly interchangeable from the caller's view?
     If no → they may not truly share the same interface (see LSP).
```
