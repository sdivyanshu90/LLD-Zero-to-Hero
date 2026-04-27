# Task Management

## Problem Summary

Design a task-management system similar to a simplified Trello checklist where tasks can be nested and completion percentage should be computed recursively.

This problem is a direct Composite Pattern exercise.

## Why This Problem Is Asked

Recursive completion percentage is the acid test for Composite Pattern mastery. An empty group must not cause a division-by-zero error, and a deeply nested tree must aggregate correctly at every level. Interviewers also probe whether the candidate's `completion_pct()` is a pure derived computation rather than a stored field that could drift out of sync.

This problem maps directly to project management tools (Jira epics → stories → subtasks) and is often used as a warm-up before harder concurrency or scheduling problems.

## Functional Requirements

1. Represent simple leaf tasks.
2. Represent composite tasks that can contain child tasks or child groups.
3. Mark tasks complete.
4. Compute completion percentage recursively for any subtree.
5. Display the task tree for debugging.

## Constraints

- Do not special-case one fixed nesting depth.
- Composite and leaf types should share a common contract.
- Completion percentage should come from the tree, not from a manually stored aggregate.

## ASCII UML

```text
+-------------------+
| TaskComponent     | <<abstract>>
+-------------------+
| title             |
+-------------------+
| completion_pct()  |
| display()         |
+-------------------+
        ^
        |
+-------+-------+
|               |
+---------------+   +-------------------+
| SimpleTask    |   | TaskGroup         |
+---------------+   +-------------------+
| done          |   | children          |
+---------------+   +-------------------+
                    | add_child()       |
                    +-------------------+

+-------------------+
| TaskBoard         |
+-------------------+
| top_level_items   |
+-------------------+
| add()             |
| overall_pct()     |
| render()          |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                        |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `SimpleTask` knows only its own completion state. `TaskGroup` knows only how to aggregate children. `TaskBoard` manages the top-level list.           |
| **OCP**   | Adding a `MilestoneTask` that blocks children from completing requires only a new subclass — `TaskBoard` and existing task types are unchanged.       |
| **LSP**   | `SimpleTask` and `TaskGroup` both satisfy the `TaskComponent` contract: `completion_pct()` returns a float in `[0, 1]`, `display()` returns a string. |
| **ISP**   | `TaskComponent` exposes only what callers need. Children management (`add_child()`) lives only on `TaskGroup`, not on the shared interface.           |
| **DIP**   | `TaskBoard` iterates over `TaskComponent` references; it never downcasts to `TaskGroup` or `SimpleTask`.                                              |

## Key Edge Cases

- An empty task group should not divide by zero.
- Marking a group complete should propagate meaningfully or be rejected explicitly.
- Deep nesting should still compute percentage correctly.

## Follow-up Questions

1. How would you add assignees and due dates?
2. How would you support weighted tasks?
3. How would you store comments or attachments?
