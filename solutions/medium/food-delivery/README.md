# Food Delivery Solution

This implementation enforces a five-state order machine and uses observers to deliver GPS updates only once the order is out for delivery.

## Design Notes

- `Order` stores the current lifecycle state.
- `CustomerSubscriber` collects location notifications.
- `DeliveryService` owns transition validation and observer dispatch.

## Complexity Analysis

| Operation                             | Time                                                      | Space                                                  |
| ------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------ |
| `transition(order_id, new_status)`    | O(1) dict lookup + O(s) observer fan-out, s = subscribers | O(1)                                                   |
| `notify_location(order_id, location)` | O(s) subscriber fan-out                                   | O(1)                                                   |
| `subscribe(order_id, subscriber)`     | O(1) list append                                          | O(1)                                                   |
| Space (total)                         | —                                                         | O(o + o×s) where o = orders, s = subscribers per order |

## SOLID Compliance

| Principle | Evidence                                                                                                                                |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Order` holds lifecycle state only. `DeliveryService` owns transitions and dispatch. `CustomerSubscriber` handles notification receipt. |
| **OCP**   | Adding an SMS notifier means one new `Subscriber` class; `DeliveryService` fan-out loop is unchanged.                                   |
| **LSP**   | All subscribers implement `notify_location(order_id, location)`; the service never branches on subscriber type.                         |
| **ISP**   | `Subscriber` declares one method. Subscribers are not forced to implement order creation or transition logic.                           |
| **DIP**   | `DeliveryService` dispatches through `Subscriber` references; it never imports `CustomerSubscriber` directly in its fan-out loop.       |

## Design Patterns

- **State machine**: `OrderStatus` enum drives a strict `CREATED -> ACCEPTED -> PREPARING -> OUT_FOR_DELIVERY -> DELIVERED` transition table. Any jump outside the table raises immediately.
- **Observer**: `CustomerSubscriber.notify_location()` receives GPS pushes; the service fan-outs only while the order is in `OUT_FOR_DELIVERY`.

## Folder Layout

```text
food-delivery/
|-- app.py
|-- models/
|   |-- order.py
|   `-- subscriber.py
`-- services/
    `-- delivery_service.py
```

## Trade-offs

- GPS updates are synchronous in this version; use an async event queue or thread pool for real-time delivery tracking at scale.
- Subscriptions are per-order; add a customer-level subscription to receive updates across multiple concurrent orders.

## Run

From this directory:

```bash
python3 app.py
```
