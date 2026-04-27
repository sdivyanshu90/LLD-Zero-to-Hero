# Splitwise

## Problem Summary

Design a Splitwise-style expense manager that records shared expenses and simplifies debts.

If the raw balances imply `A -> B -> C`, the system should simplify the result to the smallest direct set of settlements, such as `A -> C`.

## Why This Problem Is Asked

Debt simplification is a greedy graph problem disguised as a product feature. The naive approach — paying each debt separately — requires O(n²) transactions in the worst case. The optimal algorithm uses two heaps (max-heap of creditors, min-heap of debtors) to always settle the largest creditor against the largest debtor, producing the minimum number of transactions.

Interviewers also probe floating-point safety: all amounts should be stored as integer cents, not floats, to avoid rounding errors on split shares. This is an explicit correctness requirement, not just an optimization.

## Functional Requirements

1. Register members.
2. Record an expense with payer, amount, and per-member shares.
3. Maintain net balances for each member.
4. Simplify balances into a minimal direct-settlement list.
5. Expose balances and settlements for debugging.

## Constraints

- Avoid pairwise debt matrices that are repeatedly rescanned.
- Use a simplification strategy such as two heaps or equivalent creditor/debtor queues.
- Keep expense recording separate from debt simplification.

## ASCII UML

```text
+-------------------+
| Member            |
+-------------------+
| member_id         |
| name              |
+-------------------+

+-------------------+
| Expense           |
+-------------------+
| description       |
| paid_by           |
| amount_cents      |
| shares            |
+-------------------+

+-------------------+        +-------------------+
| SplitwiseService  |<>----->| Settlement        |
+-------------------+        +-------------------+
| members           |        | from_member_id    |
| balances          |        | to_member_id      |
+-------------------+        | amount_cents      |
| add_member()      |        +-------------------+
| record_expense()  |
| simplify_debts()  |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                      |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Expense` records one payment and validates shares. `SplitwiseService` owns balance tracking and simplification. `Settlement` is a pure output DTO. |
| **OCP**   | Adding percentage-based splits means a new `Expense.from_percentages()` factory; `SplitwiseService.record_expense()` is unchanged.                  |
| **LSP**   | Any expense type (equal split, custom share, percentage) must produce the same net balance effect when passed to `record_expense()`.                |
| **ISP**   | `SplitwiseService` exposes `add_member()`, `record_expense()`, `simplify_debts()`, and `snapshot_balances()`. Balance internals are hidden.         |
| **DIP**   | `SplitwiseService.simplify_debts()` works with member IDs (strings) in the heap, not with `Member` objects, decoupling it from the member model.    |

## Key Edge Cases

- Shares must sum exactly to the recorded expense.
- Unknown members must fail fast.
- Zero-net members should disappear from simplified settlements.

## Follow-up Questions

1. How would you support percentage-based splits?
2. How would you persist settlement history?
3. How would you make the service concurrent?
