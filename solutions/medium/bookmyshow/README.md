# BookMyShow Solution

This implementation models seat locks with explicit expiry timestamps and a background cleaner thread that reverts expired locks to `AVAILABLE`.

## Design Notes

- `Seat` holds current state and lock metadata.
- `BookingService` owns synchronization and lock expiry.
- A background daemon thread periodically clears stale locks.

## Complexity Analysis

| Operation               | Time                                        | Space             |
| ----------------------- | ------------------------------------------- | ----------------- |
| `lock_seat(seat_id)`    | O(1) dict lookup + lock acquire             | O(1)              |
| `confirm_seat(seat_id)` | O(1)                                        | O(1)              |
| `release_seat(seat_id)` | O(1)                                        | O(1)              |
| Background expiry scan  | O(s), s = total seats, per polling interval | O(1)              |
| Space (total)           | —                                           | O(s) for seat map |

## SOLID Compliance

| Principle | Evidence                                                                                                                  |
| --------- | ------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Seat` is state + metadata only. `BookingService` owns locking, transitions, and the expiry thread.                       |
| **OCP**   | Adding a VIP seat type requires a new seat subclass; `BookingService`’s transition logic is unchanged.                    |
| **LSP**   | Any seat subtype must honour the `AVAILABLE -> LOCKED -> BOOKED` lifecycle; skipping states would break `BookingService`. |
| **ISP**   | `BookingService` exposes three public operations. The internal cleaner thread and lock are implementation details.        |
| **DIP**   | `BookingService` operates on `Seat` objects through their status interface; it does not inspect VIP or category fields.   |

## Design Pattern

State machine + background janitor: `Seat.status` transitions `AVAILABLE -> LOCKED -> BOOKED`. A daemon thread polls for seats whose `locked_until` has passed and reverts them to `AVAILABLE` under a per-seat lock.

## Folder Layout

```text
bookmyshow/
|-- app.py
|-- models/
|   `-- seat.py
`-- services/
    `-- booking_service.py
```

## Trade-offs

- The cleaner thread uses a polling interval; replace with a priority queue of expiry times for exact-expiry semantics.
- `BookingService` holds one lock for the entire seat map during state transitions; acceptable at this scale, but per-seat locks would reduce contention in production.

## Run

From this directory:

```bash
python3 app.py
```
