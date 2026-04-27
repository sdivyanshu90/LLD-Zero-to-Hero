# Task Management Solution

This implementation uses the Composite Pattern so leaf tasks and nested task groups share one interface for progress calculation and rendering.

## Design Notes

- `TaskComponent` is the shared contract.
- `SimpleTask` is the leaf.
- `TaskGroup` is the composite.
- `TaskBoard` manages top-level items and exposes overall progress.

## Complexity Analysis

| Operation                     | Time                             | Space                |
| ----------------------------- | -------------------------------- | -------------------- |
| `completion_pct()` on a leaf  | O(1)                             | O(1)                 |
| `completion_pct()` on a group | O(n), n = total nodes in subtree | O(d) recursion depth |
| `TaskBoard.overall_pct()`     | O(n) total nodes                 | O(d) max depth       |
| Space (tree)                  | —                                | O(n)                 |

## SOLID Compliance

| Principle | Evidence                                                                                                                                                   |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `SimpleTask` knows only its own done/undone state. `TaskGroup` knows only how to aggregate children. `TaskBoard` manages the top-level list and rendering. |
| **OCP**   | Adding a `WeightedTask` requires one new `TaskComponent` subclass with a custom `completion_pct()` — `TaskGroup` and `TaskBoard` are unchanged.            |
| **LSP**   | Both `SimpleTask` and `TaskGroup` honour the `TaskComponent` contract: `completion_pct()` ∈ [0.0, 1.0] and `display()` returns a non-empty string.         |
| **ISP**   | `TaskComponent` exposes only `completion_pct()` and `display()`. The `add_child()` method is on `TaskGroup` only — `SimpleTask` never needs it.            |
| **DIP**   | `TaskBoard` iterates `list[TaskComponent]`; it never downcasts to `SimpleTask` or `TaskGroup`.                                                             |

## Design Pattern

Composite Pattern: `TaskComponent` is the shared abstract base. `SimpleTask.completion_pct()` returns 0 or 100. `TaskGroup.completion_pct()` averages its children recursively — works at any nesting depth without extra code.

## Folder Layout

```text
task-management/
|-- app.py
|-- models/
|   |-- task_component.py
|   |-- simple_task.py
|   `-- task_group.py
`-- services/
    `-- task_board.py
```

## Trade-offs

- Empty groups return 0% rather than raising; this avoids division-by-zero at the cost of distinguishing "nothing done" from "no tasks exist".
- `TaskBoard` is essentially a thin root group; merge them if a single root is always assumed.

## Run

From this directory:

```bash
python app.py
```
