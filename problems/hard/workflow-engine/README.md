# Workflow Engine

## Problem Summary

Design a DAG workflow engine that topologically schedules tasks and runs independent tasks in parallel while synchronizing between dependency levels.

## Why This Problem Is Asked

DAG execution engines underpin every CI/CD pipeline, data orchestration tool (Airflow, Prefect), and ML training framework. The interview test is whether the candidate can derive a correct topological execution order using in-degree reduction and then apply parallelism correctly at the wave level.

Cycle detection is mandatory: a cycle in the dependency graph means the execution would loop forever. Strong candidates detect cycles after executing all tasks by comparing completed task count against total task count.

## Functional Requirements

1. Register tasks with their dependency lists.
2. Validate the dependency graph and reject it if a cycle exists.
3. Execute tasks in topological order, respecting all declared dependencies.
4. Run tasks within the same dependency wave concurrently using a thread pool.
5. Collect and return all task results in topological order after the final wave completes.

## ASCII UML

```text
+-------------------+
| WorkflowTask      |
+-------------------+
| task_id           |
| dependencies      |
| action            |
+-------------------+

+-------------------+
| WorkflowEngine    |
+-------------------+
| tasks             |
| dependents        |
+-------------------+
| execute()         |
| _next_wave()      |
+-------------------+
```

## Concurrency Checklist

- Shared state: result collection must be synchronized.
- Deadlock risk: join only on worker threads launched for the current wave.
- Lock granularity: do not serialize all task actions behind one global lock.
- Lock-free alternative: a production executor would use a work-stealing queue.

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                     |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `WorkflowTask` is a data class with a callable action. `WorkflowEngine` owns graph traversal, wave scheduling, and cycle detection.                |
| **OCP**   | Adding conditional task execution (skip a task based on previous results) means wrapping the action callable; the engine’s wave loop is unchanged. |
| **LSP**   | Any `WorkflowTask` with a valid `task_id`, `dependencies`, and `action` callable satisfies the engine’s contract.                                  |
| **ISP**   | `WorkflowEngine` exposes only `register()` and `execute()`; callers never inspect wave internals or in-degree maps.                                |
| **DIP**   | `WorkflowEngine` calls `task.action()` through the callable protocol; it does not know the concrete function type.                                 |

## Key Edge Cases

- A task graph that contains a cycle must raise an error before any task runs.
- An exception in one task within a wave must not prevent other independent tasks in that wave from running.
- The result list must preserve topological ordering regardless of thread execution order.

## Follow-up Questions

1. How would you add retry logic with exponential backoff for tasks that fail transiently?
2. How would you support conditional branching where one task's output determines which downstream tasks are activated?
3. How would you distribute task execution across multiple machines using a message queue?
