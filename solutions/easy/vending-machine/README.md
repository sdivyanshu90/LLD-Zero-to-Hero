# Vending Machine Solution

This implementation keeps the workflow in explicit state objects: `IdleState`, `HasMoneyState`, and `DispensingState`.

## Design Notes

- `Product` owns stock checks and quantity decrement.
- `VendResult` describes the outcome of dispensing.
- `VendingMachine` is the context object.
- Each state object controls which operations are legal at that moment.

## Complexity Analysis

| Operation          | Time             | Space                                 |
| ------------------ | ---------------- | ------------------------------------- |
| `insert_money()`   | O(1)             | O(1)                                  |
| `select_product()` | O(1) dict lookup | O(1)                                  |
| `dispense()`       | O(1)             | O(1)                                  |
| `cancel()`         | O(1)             | O(1)                                  |
| Space (total)      | —                | O(p) for inventory, p = product count |

## SOLID Compliance

| Principle | Evidence                                                                                                                                           |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `IdleState` knows only idle-phase rules. `HasMoneyState` knows only mid-transaction rules. `VendingMachine` is a thin context that delegates.      |
| **OCP**   | A `MaintenanceState` requires only one new class; no existing state or `VendingMachine` logic changes.                                             |
| **LSP**   | All states implement `VendingState`; `VendingMachine.insert_money()` always routes through the same interface regardless of which state is active. |
| **ISP**   | `VendingState` exposes exactly the three customer operations. Inventory helpers are private to `VendingMachine`.                                   |
| **DIP**   | `VendingMachine` holds a `VendingState` reference; state transitions are the only place concrete types are instantiated.                           |

## Design Pattern

State Pattern: `IdleState`, `HasMoneyState`, and `DispensingState` each implement the same `VendingState` interface. Illegal transitions raise immediately in the wrong state — no `if machine.state == ...` chains anywhere.

## Folder Layout

```text
vending-machine/
|-- app.py
|-- models/
|   |-- product.py
|   `-- vend_result.py
`-- services/
    |-- states.py
    `-- vending_machine.py
```

## Trade-offs

- Change is returned as a single integer (total cents). For real coin-inventory management, the machine needs a denomination breakdown and a separate coin inventory.
- `DispensingState` transitions back to `Idle` immediately. Add a hardware-confirmation callback if physical dispensing can fail.

## Run

From this directory:

```bash
python app.py
```
