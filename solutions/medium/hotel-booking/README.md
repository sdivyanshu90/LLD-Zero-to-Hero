# Hotel Booking Solution

This implementation separates room availability from pricing. The pricing strategy applies a 20% surge if any night in the stay is a weekend or configured holiday.

## Design Notes

- `Room` owns overlap checks and bookings.
- `PricingStrategy` encapsulates quote calculation.
- `HotelBookingService` coordinates search, quote, and reservation.

## Complexity Analysis

| Operation                          | Time                                  | Space                 |
| ---------------------------------- | ------------------------------------- | --------------------- |
| `room.is_available(start, end)`    | O(b), b = bookings for room           | O(1)                  |
| `search_rooms(start, end)`         | O(r × b), r = rooms, b = avg bookings | O(r) results          |
| `strategy.quote(room, start, end)` | O(n), n = number of nights            | O(1)                  |
| `reserve(room_id, start, end)`     | O(b) check + O(1) append              | O(1)                  |
| Space (total)                      | —                                     | O(r + total bookings) |

## SOLID Compliance

| Principle | Evidence                                                                                                                                                                      |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Room` owns availability and booking records. `PricingStrategy` owns price calculation. `HotelBookingService` coordinates; it imports neither pricing logic nor overlap math. |
| **OCP**   | A `LoyaltyPricingStrategy` is one new class injected at service construction; the existing strategies and service are untouched.                                              |
| **LSP**   | `BasePricingStrategy` and `SurgePricingStrategy` are interchangeable; both return a valid non-negative integer for any date range.                                            |
| **ISP**   | `PricingStrategy.quote()` is the entire interface; callers never need to know if surge logic is active.                                                                       |
| **DIP**   | `HotelBookingService` accepts `PricingStrategy` at construction; it never imports the concrete strategy class directly.                                                       |

## Design Patterns

- **Strategy**: `BasePricingStrategy` and `SurgePricingStrategy` implement `PricingStrategy.quote()`. The service accepts any strategy, satisfying OCP.
- **Separation of Concerns**: availability (`Room.is_available`) is independent of pricing (`PricingStrategy.quote`); neither leaks into the other.

## Folder Layout

```text
hotel-booking/
|-- app.py
|-- models/
|   |-- room.py
|   `-- booking.py
`-- services/
    |-- pricing.py
    `-- hotel_booking.py
```

## Trade-offs

- Surge is applied if _any_ night in the stay is a weekend or holiday; a more granular model would price each night independently and sum them.
- Holidays are passed as a `set` of dates; for production, load from a configurable calendar source.

## Run

From this directory:

```bash
python3 app.py
```
