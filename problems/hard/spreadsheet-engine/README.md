# Spreadsheet Engine

## Problem Summary

Design a spreadsheet engine with a reactive dependency graph, cycle detection, and cascading recalculation when referenced cells change.

## Why This Problem Is Asked

Spreadsheet engines are one of the richest LLD problems because they require three independent skills together: expression parsing (converting formula strings to ASTs), dependency graph maintenance (reverse edges for cascading updates), and cycle detection (topological sort to reject circular references before they cause infinite loops).

Interviewers use this problem to test whether a candidate can maintain invariants across two coupled data structures — the cell values and the dependency graph — correctly when formulas change.

## Functional Requirements

1. Set a cell to a literal integer value.
2. Set a cell to a formula expressed as a list of referenced cell IDs (computed as the sum of references).
3. Detect and reject circular formula references before updating the dependency graph.
4. Cascade recalculation through all transitive dependents when a source cell changes.
5. Expose a consistent snapshot of all cell values after every update.

## ASCII UML

```text
+-------------------+
| Cell              |
+-------------------+
| cell_id           |
| value             |
| formula_refs      |
+-------------------+

+-------------------+
| Spreadsheet       |
+-------------------+
| cells             |
| dependents        |
+-------------------+
| set_value()       |
| set_formula()     |
| recalculate()     |
+-------------------+
```

## Concurrency Checklist

- Shared state: cell values and dependency edges must stay consistent.
- Deadlock risk: avoid recursive locking across dependent cells.
- Lock granularity: coarse spreadsheet lock is acceptable for this educational version.
- Lock-free alternative: versioned recalculation graphs are possible but much more complex.

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Cell` holds a raw formula string and its cached value. `DependencyGraph` owns edges and topological traversal. `SpreadsheetEngine` coordinates set, evaluate, and recalculate. |
| **OCP**   | Adding new formula functions (e.g., `AVERAGE`, `IF`) means extending the expression evaluator; the dependency graph and recalculation logic are unchanged.                      |
| **LSP**   | Constant cells and formula cells satisfy the same `evaluate() -> value` contract; the engine never branches on cell type during recalculation.                                  |
| **ISP**   | `DependencyGraph` exposes only `add_edge()`, `remove_edges_for()`, `get_dependents()`, and `detect_cycle()`. The engine never traverses raw adjacency maps.                     |
| **DIP**   | `SpreadsheetEngine` interacts with cells through their `evaluate()` interface; it is not coupled to formula parsing internals.                                                  |

## Key Edge Cases

- A formula that creates a direct or indirect cycle must be rejected before the dependency graph is updated.
- Changing a source cell must cascade to all transitive dependents, not just direct ones.
- Setting a literal value on a cell that previously had a formula must clear its formula references.

## Follow-up Questions

1. How would you support aggregate functions like `SUM(range)` and `AVG(range)` over a contiguous block of cells?
2. How would you add cell formatting (number, currency, date) separate from the underlying value?
3. How would you serialize and deserialize a full spreadsheet to and from JSON?
