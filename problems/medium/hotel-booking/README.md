# Hotel Booking

## Problem Summary

Design a hotel-booking system that uses a pricing strategy and applies a 20% surge on weekends or holidays.

## Why This Problem Is Asked

Hotel booking exercises two concerns simultaneously: interval availability (same as car rental) and pluggable pricing strategy. The price calculation must stay separate from availability so that changing from flat-rate to surge pricing does not require modifying the room or booking model.

Interviewers often extend this problem mid-interview with "what if pricing varies by night?" to test whether the candidate’s Strategy abstraction can handle per-night aggregation without redesigning the service layer.

## Functional Requirements

1. Register rooms.
2. Search availability by date range.
3. Compute dynamic prices with a strategy object.
4. Apply weekend and holiday surges.
5. Reserve a room without overlapping bookings.

## ASCII UML

```text
+-------------------+
| Room              |
+-------------------+
| room_id           |
| nightly_rate      |
| bookings          |
+-------------------+

+-------------------+
| PricingStrategy   |
+-------------------+
| quote()           |
+-------------------+

+-------------------+
| HotelBookingSvc   |
+-------------------+
| rooms             |
| pricing_strategy  |
+-------------------+
| search_available()|
| quote()           |
| reserve()         |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                     |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Room` owns availability and bookings. `PricingStrategy` owns price calculation. `HotelBookingService` coordinates search, quote, and reservation. |
| **OCP**   | Adding a loyalty-tier pricing strategy means one new `PricingStrategy` subclass; `HotelBookingService` accepts it via injection.                   |
| **LSP**   | `BasePricingStrategy` and `SurgePricingStrategy` are interchangeable; both return a valid integer quote for any date range.                        |
| **ISP**   | `PricingStrategy` has one method: `quote(room, start, end, holidays) -> int`. Callers do not need access to surge logic internals.                 |
| **DIP**   | `HotelBookingService` accepts a `PricingStrategy` at construction time; it never imports `SurgePricingStrategy` directly.                          |

## Key Edge Cases

- Partial overlaps must be rejected.
- Quotes should be deterministic for the same dates and holiday set.
- Availability search and pricing should stay separate concerns.

## Follow-up Questions

1. How would you add a loyalty points system where guests earn and redeem points?
2. How would you support multi-room bookings in a single reservation transaction?
3. How would you handle room upgrades requested after a booking is already confirmed?
