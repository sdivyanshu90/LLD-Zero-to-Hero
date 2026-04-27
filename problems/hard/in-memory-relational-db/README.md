# In-Memory Relational DB

## Problem Summary

Design a small in-memory relational table that uses row-level locks so concurrent writes to different rows do not block each other.

## Why This Problem Is Asked

Row-level locking is the fundamental concurrency primitive of every relational database. This problem tests whether a candidate knows the difference between table-level locking (simple but high-contention) and row-level locking (complex but allows concurrent access to independent rows).

The deadlock risk is the depth test: if two transactions lock rows in different orders, they can deadlock. A candidate who proposes a sorted acquisition order or a timeout-based detection shows real concurrency maturity.

## Functional Requirements

1. Create a named in-memory table with a schema.
2. Insert rows with arbitrary column maps and auto-assigned row IDs.
3. Read a row by its ID without blocking concurrent readers.
4. Update specific columns of an existing row.
5. Use per-row locking so concurrent updates to different rows proceed in parallel.

## ASCII UML

```text
+-------------------+
| Row               |
+-------------------+
| row_id            |
| values            |
| lock              |
+-------------------+

+-------------------+
| Table             |
+-------------------+
| rows              |
| table_lock        |
+-------------------+
| insert()          |
| read()            |
| update()          |
+-------------------+
```

## Concurrency Checklist

- Shared state: each row must have its own lock.
- Deadlock risk: avoid taking more than one row lock per simple update path.
- Lock granularity: row-level, not table-level, for writes.
- Lock-free alternative: MVCC or optimistic versioned rows could reduce contention further.

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **SRP**   | `Row` holds data and its own lock. `Table` owns the schema and row map. `TransactionManager` coordinates multi-row operations.       |
| **OCP**   | Adding index support means a new `Index` class attached to `Table`; the locking and row model are unchanged.                         |
| **LSP**   | Any storage backend for rows must support `lock()`, `read()`, and `write()`; the transaction manager never branches on storage type. |
| **ISP**   | Callers use `Table.insert()`, `select()`, `update()`, and `delete()`. Internal lock management is invisible.                         |
| **DIP**   | `TransactionManager` operates on `Row` abstractions; it does not import any concrete row storage class.                              |

## Key Edge Cases

- Updating a nonexistent row must fail without creating a partial entry.
- Concurrent updates to the same row must serialise correctly through the row lock.
- Concurrent updates to different rows must not block each other.

## Follow-up Questions

1. How would you add secondary indexes to support efficient lookups by non-primary-key columns?
2. How would you implement multi-row transactions with rollback on failure?
3. How would you add snapshot isolation using multi-version concurrency control (MVCC)?
