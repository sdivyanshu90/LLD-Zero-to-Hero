# Interface Segregation Principle (ISP)

> **The one-line idea:** No class should be forced to depend on methods it does not use. Prefer many small, focused interfaces over one large fat interface.

---

## Real-World Analogy — The Multi-Function Device Problem

```
Imagine a job contract (interface) that says:
  "You must be able to: print, scan, fax, staple, and make coffee."

A simple printer can only print.
It is FORCED to sign this contract anyway:
  - fax()      → raises NotImplementedError
  - scan()     → raises NotImplementedError
  - make_coffee()  → raises NotImplementedError

The printer is punished for capabilities it never claimed to have.
```

---

## The Fat Interface Violation

```
┌────────────────────────────────────────────────┐
│              <<interface>>                      │
│           MultiFunctionDevice                   │
│                                                 │
│  + print(document) → None                      │
│  + scan(document) → Image                      │
│  + fax(document, number) → bool                │
│  + staple(document) → None                     │
└────────────────────────────────────────────────┘
              ▲                    ▲
              │                    │
   ┌──────────────────┐  ┌──────────────────────┐
   │   SimplePrinter  │  │  OfficePrinterPro    │
   │  print() ✓       │  │  print() ✓           │
   │  scan() ✗ raises │  │  scan() ✓            │
   │  fax()  ✗ raises │  │  fax()  ✓            │
   │  staple()✗ raises│  │  staple() ✓          │
   └──────────────────┘  └──────────────────────┘

SimplePrinter is forced to implement (and lie about) three capabilities.
Every caller of SimplePrinter must handle potential errors from unused methods.
```

---

## The Fix — Segregated Interfaces

```
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│   <<interface>>  │   │   <<interface>>  │   │   <<interface>>  │
│    Printable     │   │    Scannable     │   │    Faxable       │
│  + print(doc)    │   │  + scan(doc)     │   │  + fax(doc,num)  │
└──────────────────┘   └──────────────────┘   └──────────────────┘
        ▲                      ▲                      ▲
        │                      │                      │
┌──────────────────┐    ┌──────────────────────────────────────────┐
│  SimplePrinter   │    │            OfficePrinterPro              │
│ implements       │    │ implements Printable + Scannable + Faxable│
│  Printable only  │    └──────────────────────────────────────────┘
└──────────────────┘

Each class implements ONLY the interfaces it genuinely supports.
Callers can depend on just the interface they need:

  def print_all(items: list[Printable]) → None:   # doesn't care about fax
      for item in items:
          item.print(...)
```

---

## The "Forced to Implement" Test

```
Look at each method in an interface and ask per implementor:

  "Does [ClassName] truly have this capability?"

  CanPrint? | CanScan? | CanFax? | CanStaple?
  ─────────────────────────────────────────────
  SimplePrinter    YES  |   NO   |   NO   |   NO     ← 3 forced methods!
  Scanner          NO   |  YES   |   NO   |   NO     ← 3 forced methods!
  FaxMachine       YES  |   NO   |  YES   |   NO     ← 2 forced methods!
  OfficePro        YES  |  YES   |  YES   |  YES     ← 0 forced methods

Fat interface imposes a burden on 3 of 4 implementors.
```

---

## Role-Based Interface Design

A common pattern is to design interfaces around **roles** rather than capabilities:

```
┌──────────────────────┐
│   <<interface>>       │
│     Workable          │      "things that can work"
│  + work() → None      │
└──────────────────────┘
        ▲
        │
┌──────────────────────┐   ┌──────────────────────┐
│        Human         │   │       Robot           │
│  work() → does task  │   │  work() → executes    │
│  eat()               │   │  recharge()           │
└──────────────────────┘   └──────────────────────┘

Bad design: add eat() to Workable just because Human needs it.
Robot can't eat → forced interface violation.

Better:
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   Workable       │  │    Feedable      │  │   Rechargeable   │
│  + work()        │  │  + eat()         │  │  + recharge()    │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        ▲                     ▲                     ▲
        │─────────────────────┘                     │
        │                                            │
   ┌─────────┐                                ┌──────────┐
   │  Human  │                                │  Robot   │
   │ Workable│                                │ Workable │
   │ Feedable│                                │ Recharg. │
   └─────────┘                                └──────────┘
```

---

## ISP Checklist

```
  □  Does any class implement a method with "raise NotImplementedError"
     or an empty pass body (that is not intentional)?
     If yes → the interface is likely too fat.

  □  Can you describe the interface's purpose in one noun phrase
     (e.g., "a thing that can be printed", "a thing that can be sorted")?
     If not → it may have too many responsibilities.

  □  Do callers import an interface but only ever call 2 of its 8 methods?
     If yes → the interface exposes too much; segregate it.

  □  If you split the interface, would any existing implementor need to change?
     If no → safe to split; no backward-compat cost.
```
