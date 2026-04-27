# Rule-Based Pricing Engine Solution

This implementation separates rule selection from discount computation. The engine evaluates rule predicates, picks the highest-priority match, and delegates the arithmetic to the winning strategy.

## Design Notes

- `PricingContext` carries request data.
- `PricingResult` returns both the price and the applied rule.
- `DiscountStrategy` models one discount calculation.
- `PricingRule` combines a predicate, priority, and strategy.
- `PricingEngine` resolves overlaps deterministically.

## Complexity Analysis

| Operation         | Time                                               | Space                  |
| ----------------- | -------------------------------------------------- | ---------------------- |
| `price(context)`  | O(r log r), r = number of rules (sort by priority) | O(r)                   |
| Adding a new rule | O(1)                                               | O(1)                   |
| Space (total)     | —                                                  | O(r) for rule registry |

The dominant cost is the priority sort. If rules are pre-sorted at registration time, `price()` becomes O(r) linear scan.

## SOLID Compliance

| Principle | Evidence                                                                                                                                  |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | Each `DiscountStrategy` computes one discount. `PricingEngine` selects the winner. `PricingContext` is a pure input DTO.                  |
| **OCP**   | Adding a `FlashSaleDiscount` means one new class registered with a priority — zero changes to `PricingEngine` or any existing strategy.   |
| **LSP**   | Every strategy must return a valid `PricingResult` with a non-negative total. Violating this breaks the engine’s guarantee to the caller. |
| **ISP**   | `DiscountStrategy` has one method: `apply(context) -> PricingResult`. Rules do not know about each other.                                 |
| **DIP**   | `PricingEngine` stores a list of `DiscountStrategy` abstractions; the concrete rule classes are never imported by name in the engine.     |

## Design Pattern

Strategy Pattern: each `DiscountStrategy.apply()` encapsulates one discount algorithm. The engine uses a priority sort to pick the single winning strategy, satisfying OCP — add a new rule without changing the engine.

## Folder Layout

```text
rule-based-pricing-engine/
|-- app.py
|-- models/
|   |-- pricing_context.py
|   `-- pricing_result.py
`-- services/
    |-- strategies.py
    `-- pricing_engine.py
```

## Trade-offs

- Only one rule wins (highest priority). To stack multiple rules, iterate in priority order and accumulate discounts instead of returning early.
- Predicates are inline lambdas; for a data-driven system, store them as expression strings and evaluate with a rules engine.

## Run

From this directory:

```bash
python app.py
```
