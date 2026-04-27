# LLD Zero to Hero

Python-first, strict, progressive preparation for Low-Level Design interviews.

## Learning Contract

- Learn in strict module order. Do not skip foundations.
- Use the Teach -> Example -> Drill loop for every concept.
- Do not move to the next module until the current one is understood.
- Do not give full solutions unless there has already been an attempt and the work is being reviewed.
- Require UML before code for every Medium or Hard problem.
- Apply a concurrency safety checklist to every Hard problem.

## Curriculum

### Module 1 - Memory Management and Core Execution

Cover stack vs heap, pass-by-value vs pass-by-reference, and garbage collection basics.
See [modules/01-memory-management-core-execution/README.md](modules/01-memory-management-core-execution/README.md).

### Module 2 - The 4 Pillars of OOP

Cover encapsulation, abstraction, inheritance, and polymorphism. Each topic must include a real-world analogy and a runnable code example.
See [modules/02-oop-pillars/README.md](modules/02-oop-pillars/README.md).

### Module 3 - Object Relations and UML

Cover composition, aggregation, interfaces vs abstract classes, and basic UML class diagrams.
See [modules/03-object-relations-and-uml/README.md](modules/03-object-relations-and-uml/README.md).

### Module 4 - SOLID Principles

Cover SRP, OCP, LSP, ISP, and DIP. Each principle must include a BEFORE and AFTER example.
See [modules/04-solid-principles/README.md](modules/04-solid-principles/README.md).

### Module 5 - Design Patterns

Cover creational, structural, and behavioral patterns with intent, ASCII UML, Python code, and a real-world analogy.
See [modules/05-design-patterns/README.md](modules/05-design-patterns/README.md).

### Module 6 - Concurrency and Thread Safety

Cover threads, race conditions, locks, deadlocks, thread pools, and optimistic vs pessimistic locking.
See [modules/06-concurrency-and-thread-safety/README.md](modules/06-concurrency-and-thread-safety/README.md).

## Problem Bank

### Easy Tier

1. Parking Lot
2. LRU Cache
3. Logger Library
4. Vending Machine
5. Tic-Tac-Toe
6. Library Management
7. Rule-Based Pricing Engine
8. Task Management
9. Blackjack
10. File System

### Medium Tier

11. Splitwise
12. Elevator System
13. Chess
14. BookMyShow
15. ATM Machine
16. Food Delivery
17. Car Rental
18. Snake and Ladders
19. Issue Tracker
20. Hotel Booking

### Hard Tier

21. In-Memory Message Broker
22. Task Scheduler
23. API Rate Limiter
24. Workflow Engine
25. In-Memory Relational DB
26. Ride-Sharing
27. Spreadsheet Engine
28. Custom Thread Pool Executor
29. Live Auction/Bidding
30. Distributed Cache Client

Detailed module content lives under [modules/README.md](modules/README.md). Detailed problem descriptions live under [problems/README.md](problems/README.md). Python implementations live under [solutions/README.md](solutions/README.md).

## Repository Layout

```text
.
|-- modules/
|   |-- 01-memory-management-core-execution/
|   |-- 02-oop-pillars/
|   |-- 03-object-relations-and-uml/
|   |-- 04-solid-principles/
|   |-- 05-design-patterns/
|   `-- 06-concurrency-and-thread-safety/
|-- problems/
|   |-- easy/
|   |-- medium/
|   `-- hard/
`-- solutions/
    |-- easy/
    |-- medium/
    `-- hard/
```

### modules/

- Contains the six prerequisite theory modules.
- Each module directory has a README plus runnable Python examples.
- Start here before attempting the problem bank.

### problems/

- Contains explanation-only material.
- No Python files belong here.
- Each problem folder should eventually describe requirements, constraints, edge cases, expected UML, and evaluation criteria.

### solutions/

- Contains runnable Python code plus a per-problem README.
- A solution must be split across multiple files, not one large script.
- Favor Python idioms such as `dataclass`, `abc`, `typing`, and `threading` when appropriate.