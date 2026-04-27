# Library Management Solution

This implementation keeps title metadata and physical copies separate while using a simple observer-style reservation queue to notify members when a copy returns.

## Design Notes

- `Book` is the title-level concept.
- `BookItem` is one physical copy with its own barcode and status.
- `Member` acts as the reservation observer.
- `ReservationService` manages title-level waitlists.
- `Library` coordinates checkout, return, and reservation flow.

## Complexity Analysis

| Operation                  | Time                                                           | Space                                       |
| -------------------------- | -------------------------------------------------------------- | ------------------------------------------- |
| `checkout(isbn)`           | O(n) scan for an available copy where n = copies for that ISBN | O(1)                                        |
| `return_item(barcode)`     | O(1) dict lookup                                               | O(1)                                        |
| `reserve(member_id, isbn)` | O(1) deque append                                              | O(1)                                        |
| `notify_next(isbn)`        | O(1) deque popleft                                             | O(1)                                        |
| Space (total)              | —                                                              | O(b) for book items + O(r) for reservations |

## SOLID Compliance

| Principle | Evidence                                                                                                                                             |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Book` = title metadata only. `BookItem` = copy lifecycle only. `ReservationService` = waitlist + notification. `Library` = checkout orchestration.  |
| **OCP**   | Adding SMS notifications means a new observer class; `ReservationService.notify_next()` calls the observer interface unchanged.                      |
| **LSP**   | Any implementation of the observer interface (email, push, SMS) can replace `Member.notify()` in the waitlist without breaking `ReservationService`. |
| **ISP**   | `Library` exposes only `checkout()`, `return_item()`, and `reserve()`; internal reservation logic is hidden inside `ReservationService`.             |
| **DIP**   | `ReservationService` calls the `Observer.notify()` abstraction; it never references the `Member` class directly in its notification logic.           |

## Design Patterns

- **Observer**: `Member.notify()` is the observer interface; `ReservationService.notify_next()` is the publisher.
- **Separation of Concerns**: title metadata (`Book`) is intentionally distinct from physical state (`BookItem`).

## Folder Layout

```text
library-management/
|-- app.py
|-- models/
|   |-- book.py
|   |-- book_item.py
|   `-- member.py
`-- services/
    |-- library.py
    `-- reservation_service.py
```

## Trade-offs

- Reservations are first-come-first-served (`deque`). Replace with a priority queue for VIP or fine-based ordering.
- A single `ReservationService` is shared across all titles; add per-branch instances for a multi-branch scenario.

## Run

From this directory:

```bash
python app.py
```
