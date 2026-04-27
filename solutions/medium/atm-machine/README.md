# ATM Machine Solution

This implementation uses a Chain of Responsibility to allocate notes while preserving ATM inventory if a withdrawal fails.

## Design Notes

- `CashHandler` tries its denomination, then delegates the remainder.
- `ATM` rebuilds a working chain per withdrawal using a draft inventory copy.
- Inventory mutates only after the chain proves the full amount is dispensable.

## Complexity Analysis

| Operation                        | Time                                                     | Space               |
| -------------------------------- | -------------------------------------------------------- | ------------------- |
| `withdraw(amount)`               | O(d), d = number of denominations (constant ≤3)          | O(d) for draft copy |
| Chain traversal per denomination | O(n/d) where n = requested amount; bounded by note count | O(1)                |
| Space (total)                    | —                                                        | O(d) for inventory  |

Because d is fixed (3 denominations), all operations are effectively O(1).

## SOLID Compliance

| Principle | Evidence                                                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **SRP**   | `CashHandler` allocates one denomination. `ATM` handles chain construction and inventory commit. Neither leaks into the other. |
| **OCP**   | Adding $50 or $5 notes requires only a new `CashHandler` subclass inserted at the right position in the chain.                 |
| **LSP**   | All handlers satisfy the same contract: consume as many notes of their denomination as possible and pass the remainder.        |
| **ISP**   | `CashHandler.handle(amount, draft)` is the entire interface. Callers never inspect denomination details.                       |
| **DIP**   | `ATM` assembles a list of `CashHandler` abstractions; it never calls concrete handler methods outside the chain.               |

## Design Pattern

Chain of Responsibility: `$100 handler -> $20 handler -> $10 handler`. Each handler takes as many of its denomination as possible and passes the remainder forward. Atomic commit ensures inventory is never partially deducted on failure.

## Folder Layout

```text
atm-machine/
|-- app.py
|-- models/
|   `-- withdrawal_result.py
`-- services/
    |-- handlers.py
    `-- atm.py
```

## Trade-offs

- A draft copy of the inventory is allocated per withdrawal; negligible cost at ATM scale.
- Adding a new denomination requires only a new `CashHandler`; the chain assembly in `ATM` stays unchanged.

## Run

From this directory:

```bash
python3 app.py
```
