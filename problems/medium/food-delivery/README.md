# Food Delivery

## Problem Summary

Design a food-delivery workflow with five states and observer-based GPS updates while an order is out for delivery.

## Why This Problem Is Asked

Food delivery combines a strict state machine (only certain transitions are valid) with the Observer pattern (customers only want GPS updates during `OUT_FOR_DELIVERY`). Layering two patterns correctly is what moves a candidate from mid-level to senior.

The trap is putting transition validation inside the order object or letting observers receive events for all states. A strong design keeps transitions in the service layer and gates observer dispatch behind a state check.

## Functional Requirements

1. Create an order.
2. Transition through exactly five states.
3. Reject invalid state jumps.
4. Register customer observers.
5. Push driver location updates only during `OUT_FOR_DELIVERY`.

## ASCII UML

```text
+-------------------+
| Order             |
+-------------------+
| order_id          |
| customer_id       |
| status            |
+-------------------+

+-------------------+
| OrderStatus       |
+-------------------+
| CREATED           |
| ACCEPTED          |
| PREPARING         |
| OUT_FOR_DELIVERY  |
| DELIVERED         |
+-------------------+

+-------------------+        +-------------------+
| DeliveryService   |<>----->| CustomerObserver  |
+-------------------+        +-------------------+
| orders            |        | notify_location() |
| subscriptions     |        +-------------------+
+-------------------+
| advance_status()  |
| push_location()   |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                                    |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Order` holds the current lifecycle state. `DeliveryService` owns transition validation and observer dispatch. `CustomerSubscriber` handles notification receipt. |
| **OCP**   | Adding a new `CANCELLED` state and a `refund_observer` means one new `OrderStatus` value and a new observer type — the transition table extension is minimal.     |
| **LSP**   | Any `Subscriber` implementation (push notification, email) must satisfy `notify_location(order_id, location)` without breaking dispatch logic.                    |
| **ISP**   | `Subscriber` only declares `notify_location()`. Subscribers do not need to implement order creation or status methods.                                            |
| **DIP**   | `DeliveryService` dispatches through the `Subscriber` interface; it never imports `CustomerSubscriber` directly in its notification logic.                        |

## Key Edge Cases

- GPS pushes before `OUT_FOR_DELIVERY` must fail.
- Delivered orders must not accept more transitions.
- Observers should receive only the orders they subscribed to.

## Follow-up Questions

1. How would you add estimated delivery time that recalculates as the driver moves?
2. How would you support multiple concurrent orders from the same customer?
3. How would you handle order cancellations at each stage and determine eligibility for a refund?
