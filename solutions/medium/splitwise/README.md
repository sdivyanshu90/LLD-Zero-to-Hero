# Splitwise Solution

This implementation keeps expense recording and debt simplification separate. Net balances are computed incrementally, then simplified with creditor and debtor heaps.

## Design Notes

- `Expense` captures one shared payment.
- `SplitwiseService` owns members, balances, and simplification logic.
- `Settlement` is the simplified output.

## Complexity Analysis

| Operation                 | Time                                          | Space                                |
| ------------------------- | --------------------------------------------- | ------------------------------------ |
| `record_expense(expense)` | O(k), k = number of share entries             | O(1)                                 |
| `simplify_debts()`        | O(n log n), n = members with non-zero balance | O(n) heaps                           |
| `snapshot_balances()`     | O(n log n) sort                               | O(n)                                 |
| Space (total)             | —                                             | O(m) for members + O(e) for expenses |

`simplify_debts()` produces the minimum number of transactions using the two-heap greedy algorithm; each heap operation is O(log n).

## SOLID Compliance

| Principle | Evidence                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Expense` records and validates one payment. `SplitwiseService` manages balances and simplification. `Settlement` is a pure output DTO.           |
| **OCP**   | Percentage-based splits add a `from_percentages()` factory on `Expense`; `record_expense()` is unchanged because it only reads the `shares` dict. |
| **LSP**   | Any expense type must produce a valid `shares` dict that sums to `amount_cents`; the service validates this before mutating balances.             |
| **ISP**   | `SplitwiseService` exposes four focused methods. The internal heap logic is fully hidden.                                                         |
| **DIP**   | `simplify_debts()` works with member ID strings in the heap; it is not coupled to the `Member` class, so membership details can change freely.    |

## Design Pattern

Two-heap debt minimization: `simplify_debts()` maintains a max-heap of creditors (positive balance) and a min-heap of debtors (negative balance). Each iteration settles the largest creditor against the largest debtor, producing the minimum number of transactions.

## Folder Layout

```text
splitwise/
|-- app.py
|-- models/
|   |-- member.py
|   |-- expense.py
|   `-- settlement.py
`-- services/
    `-- splitwise.py
```

## Trade-offs

- All amounts are stored as integer cents to avoid floating-point rounding on split shares.
- `record_expense()` validates that shares sum to the total before mutating any balance; a single failed expense leaves all balances unchanged.

## Run

From this directory:

```bash
python app.py
```
