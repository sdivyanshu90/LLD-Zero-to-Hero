# BookMyShow

## Problem Summary

Design a seat-booking system where a seat enters `LOCKED` state for a limited time and automatically reverts to `AVAILABLE` if the booking is not confirmed.

## Why This Problem Is Asked

Seat booking with expiry is the canonical concurrent reservation problem. It appears in every ticket-booking, hotel, and healthcare scheduling system. The two interview tests are: (1) modelling the three-state lifecycle (`AVAILABLE -> LOCKED -> BOOKED`) explicitly, and (2) cleaning up expired locks without corrupting concurrent state.

A candidate who uses a background thread with a polling loop and a shared lock shows practical concurrency awareness. One who uses a simple boolean flag misses the TOCTOU risk when two users request the same seat simultaneously.

## Functional Requirements

1. Lock a seat for a user.
2. Prevent another user from taking a locked seat.
3. Confirm a locked seat as `BOOKED`.
4. Run a background expiry process that reverts expired locks.
5. Expose current seat state.

## ASCII UML

```text
+-------------------+
| Seat              |
+-------------------+
| seat_id           |
| status            |
| locked_by         |
| locked_until      |
+-------------------+

+-------------------+
| SeatStatus        |
+-------------------+
| AVAILABLE         |
| LOCKED            |
| BOOKED            |
+-------------------+

+-------------------+
| BookingService    |
+-------------------+
| seats             |
| lock_duration     |
| cleaner_thread    |
+-------------------+
| lock_seat()       |
| confirm_booking() |
| snapshot()        |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Seat` holds state and lock metadata. `BookingService` owns the transition logic, the lock, and the background cleaner thread.                |
| **OCP**   | Adding VIP seat categories requires a new seat subtype and a new pricing lookup — `BookingService.lock_seat()` is unchanged.                  |
| **LSP**   | Any concrete seat type must honour the three-state lifecycle; a seat that skips `LOCKED` and goes directly to `BOOKED` violates the contract. |
| **ISP**   | `BookingService` exposes only `lock_seat()`, `confirm_seat()`, and `release_seat()`. The cleaner thread is an internal implementation detail. |
| **DIP**   | `BookingService` operates on seats through the `Seat` interface; it never inspects the concrete subtype to decide how to transition state.    |

## Key Edge Cases

- Confirming an expired lock must fail.
- Locking an already booked seat must fail.
- The background expiry loop must not corrupt shared state.

## Follow-up Questions

1. How would you support seat categories such as VIP and general with different pricing?
2. How would you notify users via email or push when their locked seat expires?
3. How would you handle two concurrent lock requests for the same seat under high load?
