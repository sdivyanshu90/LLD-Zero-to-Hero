# Rule-Based Pricing Engine

## Problem Summary

Design a pricing engine that applies discounts through the Strategy pattern while resolving overlapping rules with a clear priority hierarchy.

For example, a basket might qualify for both a loyalty discount and a coupon, but only the highest-priority rule should win.

## Why This Problem Is Asked

Pricing engines are one of the most common real-world systems interviewees are asked to design. The Strategy pattern lets each discount rule be self-contained and testable independently. The priority mechanism tests whether the candidate knows how to choose one strategy from a set without putting the selection logic inside any individual strategy.

A strong candidate also answers the OCP question: adding a flash-sale rule must not require changing the engine or any existing rule class.

## Functional Requirements

1. Accept a pricing context with subtotal and customer attributes.
2. Evaluate all discount rules.
3. Pick the highest-priority applicable rule.
4. Return both the final price and the winning rule.
5. Fall back to a no-discount strategy when no rule applies.

## Constraints

- Keep rule selection separate from discount calculation.
- Avoid hardcoding one long conditional block.
- Strategies should be easy to add without changing existing ones.

## ASCII UML

```text
+-------------------+     +-------------------+
| PricingContext    |     | PricingResult     |
+-------------------+     +-------------------+
| subtotal_cents    |     | final_total_cents |
| customer_type     |     | applied_rule      |
| coupon_code       |     +-------------------+
+-------------------+

+-------------------+
| DiscountStrategy  | <<abstract>>
+-------------------+
| apply()           |
+-------------------+
        ^
        |
+-------+-------+
|               |
+---------------+   +-------------------+
| BulkDiscount  |   | CouponDiscount    |
+---------------+   +-------------------+

+-------------------+
| PricingEngine     |
+-------------------+
| rules             |
+-------------------+
| price()           |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                        |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | Each `DiscountStrategy` computes one discount. `PricingEngine` only orchestrates rule selection. `PricingContext` is pure input data. |
| **OCP**   | Adding a `FlashSaleDiscount` means writing one new strategy class and registering it — the engine code never changes.                 |
| **LSP**   | All strategies must honour the contract: given a `PricingContext`, return a valid `PricingResult` with a non-negative total.          |
| **ISP**   | `DiscountStrategy` has a single `apply()` method. Rules do not need to know about each other or about the engine.                     |
| **DIP**   | `PricingEngine` holds a list of `DiscountStrategy` abstractions, not concrete rule classes.                                           |

## Key Edge Cases

- Multiple rules applying at once must still produce one deterministic result.
- Discounts must never drop the total below zero.
- Empty or low-value baskets should still return a valid price.

## Follow-up Questions

1. How would you support stacked discounts?
2. How would you make rules data-driven from a database?
3. How would you explain discount decisions for auditing?
