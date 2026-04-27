# Spreadsheet Engine Solution

This implementation keeps a dependency graph, rejects cyclic formulas, and recalculates cached values whenever a referenced cell changes.

## Design Notes

- `Cell` stores a `value` and `formula_refs` (list of cell IDs it depends on).
- `Spreadsheet.dependents` is a reverse-adjacency map: `{cell_id: set_of_cells_that_depend_on_it}`.
- `set_formula()` runs a full DFS cycle check on the proposed graph before mutating any state.
- `_recalculate_all()` uses Kahn's BFS topological sort to recompute all formula cells in dependency order.

## Complexity Analysis

| Operation                         | Time                                                          | Space                                 |
| --------------------------------- | ------------------------------------------------------------- | ------------------------------------- |
| `set_value(cell, value)`          | O(t) where t = total affected cells (topological propagation) | O(c) for BFS queue                    |
| `set_formula(cell, refs, fn)`     | O(c + e) DFS cycle check, then O(t) recalculation             | O(c) visited set                      |
| `_recalculate_all()` (Kahn’s BFS) | O(c + e), c = cells, e = dependency edges                     | O(c) in-degree map                    |
| Space (total)                     | —                                                             | O(c + e) for cells + dependency graph |

## SOLID Compliance

| Principle | Evidence                                                                                                                                                                               |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Cell` holds value and formula references. `DependencyGraph` (embedded in `Spreadsheet.dependents`) owns edge management. `Spreadsheet` coordinates set, cycle check, and recalculate. |
| **OCP**   | Adding `SUM`, `AVERAGE`, or `IF` functions means new entries in the formula evaluator registry; `Spreadsheet` and `Cell` are unchanged.                                                |
| **LSP**   | Constant cells and formula cells both satisfy `evaluate() -> value`; the recalculation loop never branches on cell type.                                                               |
| **ISP**   | `Spreadsheet` exposes `set_value()`, `set_formula()`, and `get_value()`. Dependency graph internals are hidden.                                                                        |
| **DIP**   | `Spreadsheet` calls cells via their evaluation interface; it does not import formula-parsing internals into its recalculation loop.                                                    |

## Design Pattern

Reactive dependency graph with topological recalculation: storing both forward (`formula_refs`) and reverse (`dependents`) edges allows O(n) cascaded recomputation via BFS. Cycle detection uses a DFS with a `visiting` set to catch back-edges before any state change.

## Folder Layout

```text
spreadsheet-engine/
|-- app.py
|-- models/
|   `-- core.py        # Cell
`-- services/
    `-- spreadsheet.py # Spreadsheet
```

## Trade-offs

- `_recalculate_all()` recomputes every cell on every change; a delta-propagation approach (traversing only the transitive dependents of the changed cell) would be more efficient for large sheets.
- Formulas are expressed as lists of referenced cell IDs (sum semantics). Supporting richer expression languages would require a parser and evaluator.
- No thread safety; add a sheet-level `RLock` for concurrent read/write access.

## Run

From this directory:

```bash
python3 app.py
```
