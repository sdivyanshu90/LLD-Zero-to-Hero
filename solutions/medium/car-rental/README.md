# Car Rental Solution

This implementation stores reservation ranges per car and answers availability by checking interval overlap instead of using a single booked flag.

## Design Notes

- `RentalBooking` represents one reservation interval.
- `Car` owns its own bookings and overlap logic.
- `CarRentalService` manages search and reservation across cars.

## Complexity Analysis

| Operation                      | Time                                 | Space                 |
| ------------------------------ | ------------------------------------ | --------------------- |
| `car.is_available(start, end)` | O(b), b = bookings per car           | O(1)                  |
| `search_available(start, end)` | O(c × b), c = cars, b = avg bookings | O(c) results          |
| `reserve(car_id, start, end)`  | O(b) overlap check + O(1) append     | O(1)                  |
| Space (total)                  | —                                    | O(c + total bookings) |

## SOLID Compliance

| Principle | Evidence                                                                                                                                |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Car` owns its bookings and overlap logic. `CarRentalService` handles search, lookup, and reservation coordination.                     |
| **OCP**   | Hourly rentals require changing the `date` type to `datetime` in `RentalBooking`; the overlap formula and service layer are untouched.  |
| **LSP**   | All car categories (economy, SUV, luxury) implement the same `is_available()` and `book()` contract; the service treats them uniformly. |
| **ISP**   | `Car` exposes only `is_available()` and `book()`. The internal booking list is encapsulated.                                            |
| **DIP**   | `CarRentalService` references cars by their public contract; it never inspects the internal `bookings` list directly.                   |

## Design Pattern

Interval overlap guard: `Car.is_available(start, end)` checks whether any existing booking overlaps `[start, end)`. Two ranges overlap if and only if `A.start < B.end and B.start < A.end`, so adjacent bookings are correctly allowed.

## Folder Layout

```text
car-rental/
|-- app.py
|-- models/
|   |-- car.py
|   `-- booking.py
`-- services/
    `-- car_rental.py
```

## Trade-offs

- Bookings are stored as a list per car; an interval tree would improve lookup for cars with thousands of historical bookings.
- Date arithmetic uses `datetime.date`; extend to `datetime.datetime` for hourly rentals.

## Run

From this directory:

```bash
python3 app.py
```
