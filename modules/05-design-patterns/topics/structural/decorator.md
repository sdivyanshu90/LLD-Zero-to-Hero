# Decorator Pattern

> **The one-line idea:** Attach new behaviour to an object at **runtime** by wrapping it in decorator objects — an alternative to subclassing that avoids combinatorial class explosion.

---

## Real-World Analogy — Coffee Shop

```
Base drink: Espresso   ($1.00)

You can add:
  + Milk    ($0.25)
  + Whipped cream ($0.50)
  + Caramel syrup ($0.75)

Each add-on WRAPS the previous drink:

  Caramel($0.75)
    └─ wraps Whip($0.50)
         └─ wraps Milk($0.25)
              └─ wraps Espresso($1.00)

Final cost = sum through the chain = $2.50

Each layer adds to the description and cost WITHOUT modifying Espresso.
```

---

## The Combinatorial Explosion Without Decorator

```
With inheritance you'd need a class per combination:
  EspressoWithMilk
  EspressoWithWhip
  EspressoWithMilkAndWhip
  EspressoWithMilkAndCaramel
  EspressoWithWhipAndCaramel
  EspressoWithMilkAndWhipAndCaramel
  ... (2^n combinations for n add-ons!)

With Decorator: 1 base + n decorator classes = n+1 classes total.
```

---

## Structure

```
               ┌──────────────────────────────┐
               │       <<interface>>           │
               │          Beverage             │
               │  + description() → str        │
               │  + cost() → float             │
               └──────────────────────────────┘
                       ▲             ▲
                       │             │
          ┌──────────────────┐    ┌──────────────────────────┐
          │     Espresso     │    │    CondimentDecorator     │
          │ description()→   │    │  - _wrapped: Beverage     │
          │   "Espresso"     │    │  + description() → str    │
          │ cost() → 1.00    │    │  + cost() → float         │
          └──────────────────┘    └──────────────────────────┘
                                             ▲
                              ┌──────────────┼───────────────┐
                              │              │               │
                  ┌───────────────┐  ┌───────────────┐  ┌──────────────┐
                  │     Milk      │  │   WhipCream   │  │   Caramel    │
                  │ description() │  │ description() │  │ description()│
                  │ → wrapped.desc│  │ → wrapped.desc│  │ → wrapped.d. │
                  │   + ", Milk"  │  │   + ", Whip"  │  │  + ",Caramel"│
                  │ cost()        │  │ cost()        │  │ cost()       │
                  │ → wrapped.cost│  │ → wrapped.cost│  │ → wrapped.c. │
                  │   + 0.25      │  │   + 0.50      │  │  + 0.75      │
                  └───────────────┘  └───────────────┘  └──────────────┘
```

---

## Recursive Cost Chain Walkthrough

```
order = Caramel(Whip(Milk(Espresso())))

order.cost() called:
  Caramel.cost()
    = self._wrapped.cost() + 0.75
    = Whip.cost() + 0.75
        = self._wrapped.cost() + 0.50
        = Milk.cost() + 0.50
            = self._wrapped.cost() + 0.25
            = Espresso.cost() + 0.25
            = 1.00 + 0.25
            = 1.25
        = 1.25 + 0.50
        = 1.75
    = 1.75 + 0.75
    = 2.50

Final: $2.50 ✓
```

---

## Decorator vs. Inheritance Comparison

```
┌─────────────────────────────┬───────────────────────────────┐
│         Decorator            │        Inheritance            │
├─────────────────────────────┼───────────────────────────────┤
│ Behaviour added at runtime  │ Behaviour added at compile time│
│ Any combination possible    │ 2^n classes for n variations  │
│ Decorators are composable   │ Each combination needs a class│
│ Single Responsibility       │ Subclass often mixes concerns  │
│ Open for extension (OCP)    │ Requires modifying hierarchy   │
└─────────────────────────────┴───────────────────────────────┘
```

---

## Decorator Checklist

```
  □  Does the decorator implement the SAME interface as the component it wraps?
     If not → callers can't use decorated and undecorated objects interchangeably.

  □  Does the decorator hold a reference (_wrapped) to the component?
     If not → it can't delegate behaviour.

  □  Does each decorator do exactly ONE extra thing?
     Multiple responsibilities in one decorator → violates SRP.

  □  Could you achieve the same with inheritance without class explosion?
     If yes with only 2-3 variants → inheritance may be simpler.
```
