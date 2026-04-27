# Issue Tracker Solution

This implementation keeps workflows data-driven per issue type and validates transitions through a dedicated workflow engine.

## Design Notes

- `Issue` carries type and current status.
- `WorkflowEngine` owns the dynamic allowed-transition map.
- `IssueTracker` manages issue creation and transition requests.

## Complexity Analysis

| Operation                          | Time                             | Space                                               |
| ---------------------------------- | -------------------------------- | --------------------------------------------------- |
| `create_issue()`                   | O(1)                             | O(1)                                                |
| `transition(issue_id, new_status)` | O(1) dict lookup in workflow map | O(1)                                                |
| `is_valid_transition()`            | O(1) set membership test         | O(1)                                                |
| Space (total)                      | —                                | O(i) for issues + O(t) for transition table entries |

All operations are O(1) because the workflow map is a hash-based lookup.

## SOLID Compliance

| Principle | Evidence                                                                                                                                |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Issue` holds type and status. `WorkflowEngine` validates transitions. `IssueTracker` coordinates creation and routing.                 |
| **OCP**   | New issue type or new status means one new dict entry in `WorkflowEngine` — no code changes required anywhere.                          |
| **LSP**   | All issue types are instances of the same `Issue` class; the workflow engine dispatches on `issue.issue_type` uniformly.                |
| **ISP**   | `WorkflowEngine` exposes only `is_valid_transition()` and `transition()`. `IssueTracker` does not need to read the raw transition dict. |
| **DIP**   | `IssueTracker` calls `WorkflowEngine` through its public contract; it never reads `WorkflowEngine._transitions` directly.               |

## Design Pattern

Data-driven workflow: `WorkflowEngine` stores `{(issue_type, from_status): {allowed_to_statuses}}`. Adding a new issue type or new transition requires only a dict entry, not new code. Terminal states simply have no outbound entries.

## Folder Layout

```text
issue-tracker/
|-- app.py
|-- models/
|   `-- issue.py
`-- services/
    |-- workflow_engine.py
    `-- issue_tracker.py
```

## Trade-offs

- The workflow map is compiled at startup; replace with a database-backed config for runtime changes without redeployment.
- Transition history is not stored; add a `history: list[StatusChange]` field to `Issue` to support full audit trails.

## Run

From this directory:

```bash
python3 app.py
```
