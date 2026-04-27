# Library Management

## Problem Summary

Design a small library system where a `Book` represents the title-level concept and a `BookItem` represents one physical copy.

Reservations should use the Observer pattern so waiting members can be notified when a copy becomes available.

## Why This Problem Is Asked

The Book vs BookItem distinction is a recurring data modeling question in library, e-commerce, and media systems. A single `Book` class that tracks both metadata and copy availability is a classic SRP violation that interviewers explicitly probe for.

The Observer pattern for reservations tests whether the candidate can decouple the "something became available" event from "who needs to know about it", which is the same async notification problem found in order tracking, seat releases, and queue management.

## Functional Requirements

1. Register members.
2. Add physical book copies to the library.
3. Check out an available `BookItem` by ISBN.
4. Return a `BookItem` by barcode.
5. Allow members to reserve a title when no copy is available.
6. Notify the next waiting member when a copy is returned.

## Constraints

- Do not collapse `Book` and `BookItem` into one class.
- Reservations should be title-based, not copy-based.
- Notification logic should stay separate from checkout logic.

## ASCII UML

```text
+-------------------+     +-------------------+
| Book              |     | BookItem          |
+-------------------+     +-------------------+
| isbn              |<>-->| barcode           |
| title             |     | isbn              |
+-------------------+     | status            |
                          +-------------------+

+-------------------+     +-------------------+
| Member            |     | ReservationService|
+-------------------+     +-------------------+
| member_id         |     | waitlists         |
| name              |     +-------------------+
+-------------------+     | reserve()         |
| notify()          |     | notify_next()     |
+-------------------+     +-------------------+

+-------------------+
| Library           |
+-------------------+
| books             |
| copies            |
| members           |
+-------------------+
| checkout()        |
| return_item()     |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                           |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Book` = title metadata. `BookItem` = physical copy status. `ReservationService` = notification and waitlist. `Library` = orchestration. |
| **OCP**   | Adding email notifications means a new `Observer` implementation; existing checkout and return logic is untouched.                       |
| **LSP**   | Any `Observer` implementation (SMS, email, in-app) can replace `Member.notify()` without changing `ReservationService`.                  |
| **ISP**   | `Library` exposes only `checkout()` and `return_item()`; members do not see internal waitlist management.                                |
| **DIP**   | `ReservationService.notify_next()` calls the `Observer` interface, not `Member` directly.                                                |

## Key Edge Cases

- Checking out a book with no available copy should fail.
- Returning an unknown barcode should fail.
- Duplicate reservations by the same member for the same ISBN should be rejected.

## Follow-up Questions

1. How would you add due dates and fines?
2. How would you limit reservations per member?
3. How would you support multiple branches?
