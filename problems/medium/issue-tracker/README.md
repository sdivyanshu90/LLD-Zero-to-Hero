# Issue Tracker

## Problem Summary

Design an issue tracker where each issue type has its own workflow and allowed transitions are configured dynamically.

## Why This Problem Is Asked

Jira-style workflow engines are one of the most common backend systems candidates are asked to design. The key insight is making the transition table _data-driven_: stored as a dict of `{(type, from_status): {allowed_to_statuses}}` rather than hardcoded `if/elif` chains. Adding a new issue type or a new state then requires only a new dict entry.

Terminal states (like `CLOSED` or `DONE`) are modelled elegantly by simply having no outbound transitions in the table rather than with a special flag on the status.

## Functional Requirements

1. Create issues of different types.
2. Maintain current issue status.
3. Validate transitions per issue type.
4. Reject disallowed transitions.
5. Keep workflow definitions configurable.

## ASCII UML

```text
+-------------------+
| Issue             |
+-------------------+
| issue_id          |
| issue_type        |
| status            |
+-------------------+

+-------------------+
| WorkflowEngine    |
+-------------------+
| transition_map    |
+-------------------+
| can_transition()  |
| transition()      |
+-------------------+

+-------------------+
| IssueTracker      |
+-------------------+
| issues            |
| workflow_engine   |
+-------------------+
| create_issue()    |
| transition_issue()|
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                               |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **SRP**   | `Issue` carries type, status, and metadata only. `WorkflowEngine` owns the transition table and validation. `IssueTracker` coordinates creation and routing. |
| **OCP**   | Adding a new issue type (`INCIDENT`) requires only a new entry in `WorkflowEngine`’s transition dict — no new code.                                          |
| **LSP**   | All issue types are instances of the same `Issue` class; the workflow engine treats them uniformly via the `issue_type` field.                               |
| **ISP**   | `WorkflowEngine` exposes only `is_valid_transition()` and `transition()`. `IssueTracker` does not need to know the internal dict structure.                  |
| **DIP**   | `IssueTracker` delegates all validation to `WorkflowEngine`; it never checks transition logic directly in its own methods.                                   |

## Key Edge Cases

- Different issue types can have different allowed transitions from the same status.
- Unknown issue types or statuses must fail fast.
- Terminal states should reject further transitions.

## Follow-up Questions

1. How would you add assignees and keep a full assignment history per issue?
2. How would you support sub-tasks or nested issues linked to a parent?
3. How would you add SLA-based escalation that automatically moves overdue issues to a higher priority?
