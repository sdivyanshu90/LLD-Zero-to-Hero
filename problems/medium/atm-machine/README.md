# ATM Machine

## Problem Summary

Design an ATM that dispenses cash using a Chain of Responsibility in the order `$100 -> $20 -> $10`.

## Why This Problem Is Asked

ATM disbursement tests two combined skills: Chain of Responsibility for note-denomination handling and atomic commit semantics for inventory. The trap is partial deduction — if the chain runs and partially allocates notes before discovering it cannot fill the rest, inventory should be left unchanged.

Interviewers probe for the draft-copy-then-commit pattern: allocate on a working copy, commit only on full success. Candidates who mutate inventory eagerly and then try to undo fail the correctness test.

## Functional Requirements

1. Track note inventory by denomination.
2. Withdraw only supported amounts.
3. Use chained handlers to determine note allocation.
4. Reject withdrawals that cannot be fulfilled exactly.
5. Expose remaining inventory.

## ASCII UML

```text
+-------------------+
| WithdrawalResult  |
+-------------------+
| dispensed_notes   |
| remaining_amount  |
+-------------------+

+-------------------+
| CashHandler       |
+-------------------+
| denomination      |
| next_handler      |
+-------------------+
| dispense()        |
+-------------------+

+-------------------+
| ATM               |
+-------------------+
| inventory         |
| chain_head        |
+-------------------+
| withdraw()        |
| snapshot()        |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **SRP**   | `CashHandler` handles one denomination. `ATM` builds the chain and manages inventory commit. Each has one reason to change.          |
| **OCP**   | Adding a $50 note means one new `CashHandler` subclass inserted into the chain — no changes to `ATM` or other handlers.              |
| **LSP**   | All handlers satisfy the same chain contract: try this denomination, pass the remainder forward.                                     |
| **ISP**   | `CashHandler` exposes only `handle(amount, inventory)`. Callers do not need to know which denomination a handler covers.             |
| **DIP**   | `ATM` builds a chain of `CashHandler` abstractions; it never calls `$100Handler` or `$20Handler` directly in its disbursement logic. |

## Key Edge Cases

- Unsupported amounts must fail before mutating inventory.
- Limited note counts can block an otherwise divisible withdrawal.
- A failed withdrawal must not partially deduct inventory.

## Follow-up Questions

1. How would you add support for additional denominations like $50 and $5?
2. How would you handle partial restocks mid-session where only one denomination is refilled?
3. How would you add PIN authentication as a prerequisite step before dispensing?
