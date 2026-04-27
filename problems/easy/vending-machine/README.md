# Vending Machine

## Problem Summary

Design a vending machine with a strict State Pattern flow:

`Idle -> HasMoney -> Dispensing`

The machine must accept money, allow product selection only after money is inserted, dispense the item, and return exact change.

## Why This Problem Is Asked

State Pattern is mandatory knowledge for senior engineers. The interview trap here is a `VendingMachine` full of `if self.state == 'idle': ...` branches. A candidate who encodes each state as its own class signals that they know how to eliminate conditional sprawl in real production code.

The follow-up question "what if dispensing hardware fails midway?" often separates candidates who can adapt a pattern from those who only memorised it.

## Functional Requirements

1. Load products with code, price, and quantity.
2. Insert money in cents.
3. Select a product by code.
4. Dispense the product only when enough balance is available.
5. Return exact change after dispensing.
6. Allow the customer to cancel and receive a refund before dispensing.

## Constraints

- The state transitions must be explicit in the design.
- Do not collapse the workflow into one service full of conditionals.
- Inventory checks and money checks should stay readable and isolated.

## ASCII UML

```text
+-------------------+
| VendingMachine    |
+-------------------+
| inventory         |
| balance_cents     |
| state             |
+-------------------+
| insert_money()    |
| select_product()  |
| cancel()          |
+-------------------+

+-------------------+
| VendingState      | <<abstract>>
+-------------------+
| insert_money()    |
| select_product()  |
| cancel()          |
+-------------------+
        ^
        |
+-------+-------+-------+
|               |       |
+----------+ +----------+ +----------+
| Idle     | | HasMoney | |Dispensing|
| State    | | State    | | State    |
+----------+ +----------+ +----------+

+-------------------+     +-------------------+
| Product           |     | VendResult        |
+-------------------+     +-------------------+
| code              |     | product_code      |
| name              |     | product_name      |
| price_cents       |     | change_cents      |
| quantity          |     +-------------------+
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                                               |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `IdleState`, `HasMoneyState`, and `DispensingState` each handle exactly one phase of the transaction. `VendingMachine` is a thin context that delegates to the active state. |
| **OCP**   | Adding a `MaintenanceState` requires one new class and one new transition in the context — no existing state class changes.                                                  |
| **LSP**   | All state classes implement `VendingState`; `VendingMachine` treats them uniformly through that interface.                                                                   |
| **ISP**   | `VendingState` exposes only the three operations a customer can perform. Internal helpers stay private to the machine.                                                       |
| **DIP**   | `VendingMachine` delegates to `VendingState` (an abstraction), never calls concrete state logic directly.                                                                    |

## Key Edge Cases

- Selecting a product without inserting money should fail.
- Selecting an unknown product should fail.
- Selecting an out-of-stock product should fail.
- Inserting negative or zero money should fail.

## Suggested Domain Model

- `Product`: inventory entry.
- `VendResult`: what was dispensed and how much change returned.
- `VendingState`: contract for state-specific behavior.
- `VendingMachine`: context object that owns inventory, balance, and current state.

## Follow-up Questions

1. How would you add coin-by-coin change availability instead of unlimited exact change?
2. How would you support multiple payment methods?
3. What would change if dispensing hardware could fail midway?
