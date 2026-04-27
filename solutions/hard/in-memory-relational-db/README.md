# In-Memory Relational DB Solution

This implementation keeps a table-level lock only for row creation and one lock per row for reads and writes, so unrelated row updates do not block each other.

## Design Notes

- `Row` is a dataclass with a `row_id`, a `values` dict, and its own `threading.Lock`.
- `Table` holds a `dict[row_id, Row]` protected by a single table-level `Lock` used only during `insert()` to prevent row-ID races.
- `read()` acquires the row lock (shared read semantics; Python `Lock` is exclusive, but reads are fast enough at this scale).
- `update()` acquires only the target row's lock, leaving all other rows unblocked.

## Complexity Analysis

| Operation                | Time                               | Space                  |
| ------------------------ | ---------------------------------- | ---------------------- |
| `insert(values)`         | O(1) dict insert (with table lock) | O(1)                   |
| `read(row_id)`           | O(1) dict lookup (with row lock)   | O(1)                   |
| `update(row_id, values)` | O(1) dict update (with row lock)   | O(1)                   |
| `delete(row_id)`         | O(1) dict pop (with table lock)    | O(1)                   |
| `select(predicate)`      | O(n), n = rows                     | O(r) results           |
| Space (total)            | —                                  | O(n) rows + O(n) locks |

## SOLID Compliance

| Principle | Evidence                                                                                                                                                  |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Row` owns row data and its own lock. `Table` owns the row map and schema. `TransactionManager` coordinates multi-row operations.                         |
| **OCP**   | Adding a secondary index means a new `Index` class attached to `Table.insert()`; the row and lock model are unchanged.                                    |
| **LSP**   | Any row storage backend must satisfy `read()`, `update()`, and `delete()` with the row-lock semantics; the transaction manager treats all rows uniformly. |
| **ISP**   | `Table` exposes only the four CRUD methods and `select()`. Internal row-lock management is invisible to callers.                                          |
| **DIP**   | `TransactionManager` works through the `Table` interface; it never directly accesses `Row._values` or `Row._lock`.                                        |

## Design Pattern

Row-level locking: the table lock is a creation guard, not a read/write guard. Once a row exists, its own lock serialises concurrent updates. Two threads updating different rows hold different locks and never contend.

## Folder Layout

```text
in-memory-relational-db/
|-- app.py
|-- models/
|   `-- core.py     # Row
`-- services/
    `-- database.py # Table, InMemoryDB
```

## Trade-offs

- `RLock` could replace `Lock` per row to allow the same thread to re-enter (e.g. a trigger that reads while updating). The current version uses a plain `Lock` to keep semantics explicit.
- Multi-row transactions require a canonical lock-ordering protocol (e.g. sorted row-ID order) to prevent deadlocks; not implemented here.
- No secondary indexes; full-table scans for non-primary-key queries.

## Run

From this directory:

```bash
python3 app.py
```
