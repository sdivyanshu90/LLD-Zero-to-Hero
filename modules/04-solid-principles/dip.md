# Dependency Inversion Principle (DIP)

> **The one-line idea:** High-level modules should not depend on low-level modules. Both should depend on **abstractions**. And abstractions should not depend on details — details should depend on abstractions.

---

## Real-World Analogy — Power Outlets

```
WITHOUT DIP — Your laptop is hardwired to a specific power source:
  ┌──────────────────────────────────────────────────────────┐
  │  LAPTOP  ──wire────────────────────►  WALL SOCKET (230V) │
  └──────────────────────────────────────────────────────────┘
  Move to a different country? Laptop breaks.
  The high-level module (laptop) depends on the low-level detail (socket type).

WITH DIP — Your laptop uses an abstract power interface:
  ┌───────────┐     ┌──────────────────┐     ┌────────────────────┐
  │  LAPTOP   │────►│  Power Adapter   │◄────│  Wall Socket       │
  │ (high-lv) │     │  (abstraction)   │     │  (low-level detail)│
  └───────────┘     └──────────────────┘     └────────────────────┘
  Swap the adapter → laptop works anywhere.
  High-level (laptop) depends on abstraction (adapter), not the socket.
```

---

## The Violation — Wrong Dependency Direction

```
WITHOUT DIP:

  ┌─────────────────────┐
  │   OrderService      │         HIGH-LEVEL module
  │   (business logic)  │
  │  + place_order()    │
  └─────────────────────┘
              │
              │  depends on directly ─────────────────────────────────►
              │
  ┌─────────────────────┐
  │   MySQLDatabase     │         LOW-LEVEL module
  │  + save_order()     │
  │  + find_order()     │
  └─────────────────────┘

  OrderService KNOWS about MySQL.
  Want to switch to PostgreSQL? Modify OrderService.
  Want to test OrderService? You need a real MySQL database.
```

---

## The Fix — Invert the Dependency

```
WITH DIP:

  ┌─────────────────────┐         HIGH-LEVEL module
  │   OrderService      │
  │  + place_order()    │
  └─────────────────────┘
              │
              │  depends on abstraction ──────────────────────────────►
              │
  ┌─────────────────────┐
  │  <<interface>>      │         ABSTRACTION
  │  OrderRepository    │
  │  + save(order)      │
  │  + find_by_id(id)   │
  └─────────────────────┘
              ▲
     ┌────────┴────────┐
     │                 │
  ┌─────────────┐  ┌─────────────┐
  │MySQLOrderRepo│  │InMemoryRepo │   LOW-LEVEL modules (implement abstraction)
  │ save() ✓    │  │ save() ✓    │
  │ find_by_id()│  │ find_by_id()│
  └─────────────┘  └─────────────┘

  OrderService depends on the interface, never on MySQL or InMemory.
  The dependency ARROW was reversed — hence "Inversion".
```

---

## Three Injection Mechanisms

### Constructor Injection (preferred)

```
class OrderService:
    def __init__(self, repo: OrderRepository):     ← dependency injected at creation
        self._repo = repo

# Caller decides which implementation to use:
service = OrderService(MySQLOrderRepository())     # production
service = OrderService(InMemoryOrderRepository())  # test
```

### Method Injection (when dependency varies per call)

```
class ReportGenerator:
    def generate(self, data, formatter: ReportFormatter) → str:
        return formatter.format(data)              ← different formatter per call
```

### Property Injection (use sparingly — optional dependency)

```
class DataProcessor:
    def __init__(self):
        self.logger: Logger = NullLogger()         ← sensible default

    # Caller can replace:
    processor.logger = FileLogger("output.log")
```

---

## Layered Architecture View

```
WITHOUT DIP — layers point downward:

  ┌─────────────────────────────────────────┐
  │           Presentation Layer            │  ─── depends on ──►
  └─────────────────────────────────────────┘
  ┌─────────────────────────────────────────┐
  │           Business Logic Layer          │  ─── depends on ──►
  └─────────────────────────────────────────┘
  ┌─────────────────────────────────────────┐
  │             Data Access Layer           │
  └─────────────────────────────────────────┘

WITH DIP — all layers depend on abstractions:

  ┌─────────────────────────────────────────┐
  │           Presentation Layer            │
  │     depends on: IProductService         │
  └─────────────────────────────────────────┘
                    ▲ implements
  ┌─────────────────────────────────────────┐
  │           Business Logic Layer          │
  │     depends on: IProductRepository      │
  └─────────────────────────────────────────┘
                    ▲ implements
  ┌─────────────────────────────────────────┐
  │             Data Access Layer           │
  │   concrete MySQLProductRepository       │
  └─────────────────────────────────────────┘

No layer directly names a lower-level concrete class.
```

---

## DIP Checklist

```
  □  Does any high-level class import or instantiate a concrete low-level class?
     If yes → the dependency direction is wrong; introduce an abstraction.

  □  Are you using `new ClassName()` or `ClassName()` inside a business class?
     If yes → extract to an injected interface.

  □  Can you swap the database / messaging system / email provider
     WITHOUT modifying business logic classes?
     If no → DIP is not in place.

  □  Can you test the business logic class with a simple in-memory stub?
     If no → the class is tightly coupled to infrastructure.
```
