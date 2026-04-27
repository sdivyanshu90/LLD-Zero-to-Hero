# Hard Problems

Focus area: concurrency-heavy systems, custom infrastructure, and thread-safe design.

21. [In-Memory Message Broker](in-memory-message-broker/README.md): Concurrent producers, offset tracking, and crash-safe delivery without duplication.
22. [Task Scheduler](task-scheduler/README.md): Custom delay queue plus thread pool while preventing starvation.
23. [API Rate Limiter](api-rate-limiter/README.md): Lock-free token bucket that scales under extreme concurrency.
24. [Workflow Engine](workflow-engine/README.md): DAG execution with topological ordering and parallel task scheduling.
25. [In-Memory Relational DB](in-memory-relational-db/README.md): Row-level locking so unrelated writes do not block each other.
26. [Ride-Sharing](ride-sharing/README.md): Spatial matching with optimistic locking to prevent double-booking.
27. [Spreadsheet Engine](spreadsheet-engine/README.md): Reactive dependency graph with cycle detection and cascading recalculation.
28. [Custom Thread Pool Executor](custom-thread-pool-executor/README.md): Manual worker lifecycle and configurable rejection policies.
29. [Live Auction/Bidding](live-auction-bidding/README.md): Strictly increasing bids with efficient large-scale broadcast.
30. [Distributed Cache Client](distributed-cache-client/README.md): Consistent hashing ring with localized redistribution on node failure.