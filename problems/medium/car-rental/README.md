# Car Rental

## Problem Summary

Design a car-rental system that answers date-range availability queries correctly instead of using a single `booked` flag.

## Why This Problem Is Asked

Interval overlap is the fundamental operation for any reservation system — rentals, hotel rooms, meeting rooms, or flight seats. The interview test is whether the candidate knows the overlap condition `A.start < B.end and B.start < A.end` by heart and places it correctly in the domain model (on `Car`, not on the service).

A single `booked` flag is the naive answer; it breaks as soon as a second booking is allowed after a return. The model must store reservation intervals and check them individually.

## Functional Requirements

1. Register cars.
2. Search by date range.
3. Reject overlapping reservations.
4. Allow non-overlapping reservations on the same car.
5. Expose reservation state.

## ASCII UML

```text
+-------------------+
| RentalBooking     |
+-------------------+
| booking_id        |
| car_id            |
| start_date        |
| end_date          |
+-------------------+

+-------------------+
| Car               |
+-------------------+
| car_id            |
| model             |
| bookings          |
+-------------------+
| is_available()    |
| reserve()         |
+-------------------+

+-------------------+
| CarRentalService  |
+-------------------+
| cars              |
+-------------------+
| search_available()|
| reserve_car()     |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                        |
| --------- | --------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Car` owns overlap detection and its own booking list. `CarRentalService` handles search and coordination.            |
| **OCP**   | Hourly rentals mean changing the date type to `datetime`; the overlap formula and service logic are unchanged.        |
| **LSP**   | All car types (economy, SUV, luxury) satisfy `Car.is_available(start, end) -> bool` without changing the caller.      |
| **ISP**   | `Car` exposes only `is_available()` and `book()`. The internal booking list is hidden.                                |
| **DIP**   | `CarRentalService` searches through `Car` objects by their public contract, not by inspecting booking lists directly. |

## Key Edge Cases

- Adjacent but non-overlapping bookings should be allowed.
- Reverse or zero-length ranges must fail.
- Searching should not mutate state.

## Follow-up Questions

1. How would you add daily pricing that varies by car category and rental duration?
2. How would you support different vehicle categories such as economy, SUV, and luxury?
3. How would you handle early returns and compute a partial refund for unused days?
