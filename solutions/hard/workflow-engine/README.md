# Workflow Engine Solution

This implementation executes a DAG in topological waves. Each wave runs independent tasks in parallel, then the engine synchronizes before releasing dependents.

## Design Notes

- `WorkflowTask` is a frozen dataclass with `task_id`, `dependencies`, and an `action` callable.
- `WorkflowEngine.execute()` builds a reverse-adjacency map and an in-degree map, then repeatedly dispatches the zero-in-degree "wave" of tasks.
- Each wave launches one thread per task; the engine joins all wave threads before resolving the next wave.
- Results are appended to a list under a `Lock` to avoid concurrent list mutation.

## Complexity Analysis

| Operation                              | Time                                                          | Space                             |
| -------------------------------------- | ------------------------------------------------------------- | --------------------------------- |
| `execute()` total                      | O(t + e + w×t) where t = tasks, e = edges, w = max wave width | O(t + e)                          |
| In-degree build                        | O(t + e)                                                      | O(t + e)                          |
| Wave thread launch                     | O(w) threads per wave                                         | O(w)                              |
| Cycle detection (post-execution check) | O(1) count comparison                                         | O(1)                              |
| Space (total)                          | —                                                             | O(t + e) for task map + adjacency |

## SOLID Compliance

| Principle | Evidence                                                                                                                                |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `WorkflowTask` is a data class (id, dependencies, action). `WorkflowEngine` owns graph building, wave scheduling, and cycle detection.  |
| **OCP**   | Conditional execution (skip task on previous failure) means wrapping `action` in a guard callable; the engine’s wave loop is unchanged. |
| **LSP**   | Any `WorkflowTask` with a valid `task_id`, `dependencies` set, and zero-argument `action` satisfies the engine’s contract.              |
| **ISP**   | `WorkflowEngine` exposes only `execute() -> list[list[str]]`; callers never inspect in-degree maps or adjacency lists.                  |
| **DIP**   | `WorkflowEngine` calls `task.action()` through the callable protocol; it does not import any concrete task function by name.            |

## Design Pattern

Level-synchronised parallel BFS: tasks at the same dependency depth form a wave. All tasks in a wave are independent, so they run concurrently. The engine only advances to the next wave after the current wave's threads complete, ensuring dependency ordering without per-task futures.

## Folder Layout

```text
workflow-engine/
|-- app.py
|-- models/
|   `-- core.py          # WorkflowTask
`-- services/
    `-- workflow_engine.py # WorkflowEngine
```

## Trade-offs

- Wave-level parallelism; tasks within a wave are maximally parallel. Fine-grained task-level futures (e.g. `concurrent.futures`) would offer the same throughput with less custom code.
- `threading.Thread` is used directly; replace with a thread pool to cap the number of concurrent OS threads for very wide DAGs.
- No cycle detection at registration time; call `_validate_dag()` in `register()` to catch cycles eagerly.

## Run

From this directory:

```bash
python3 app.py
```
