# Ride-Sharing Solution

This implementation finds the nearest available driver from a snapshot, then attempts an optimistic version check on each candidate to prevent double-booking.

## Design Notes

- `Location` is a frozen dataclass with Manhattan-distance helper.
- `Driver` carries `available`, `version`, and a per-driver `threading.Lock`.
- `RideMatcher.request_ride()` snapshots available drivers sorted by distance, then iterates candidates calling `_try_assign()`.
- `_try_assign()` acquires the driver lock, re-checks availability and version, and commits only if both match the snapshot values.

## Complexity Analysis

| Operation                      | Time                                                 | Space                    |
| ------------------------------ | ---------------------------------------------------- | ------------------------ |
| `request_ride(pickup)`         | O(d log d), d = available drivers (sort by distance) | O(d) snapshot            |
| `_try_assign(driver, version)` | O(1) lock + version check                            | O(1)                     |
| Distance computation           | O(1) Manhattan distance                              | O(1)                     |
| Space (total)                  | —                                                    | O(d) for driver registry |

In the worst case (all drivers unavailable after snapshot), the matcher tries all d candidates before returning `None`.

## SOLID Compliance

| Principle | Evidence                                                                                                                                                    |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Location` is a pure value with distance logic. `Driver` owns availability state and its own lock. `RideMatcher` owns proximity sorting and OCC assignment. |
| **OCP**   | Adding vehicle-type filtering means a pre-sort filter applied in `request_ride()`; the OCC `_try_assign()` loop is unchanged.                               |
| **LSP**   | Any `Driver` subtype (car, bike, moto) satisfies the same availability and version interface; `RideMatcher` treats all uniformly.                           |
| **ISP**   | `RideMatcher` exposes only `request_ride()` and `snapshot()`. Clients never read `Driver.version` directly.                                                 |
| **DIP**   | `RideMatcher` accepts `list[Driver]`; it is not coupled to any ride-management or GPS service.                                                              |

## Design Pattern

Optimistic locking with retry: the assignment reads driver state without holding a lock, then validates under the lock before committing. If another request won the driver between the snapshot and the lock, the version mismatch triggers a retry on the next candidate.

## Folder Layout

```text
ride-sharing/
|-- app.py
|-- models/
|   `-- core.py     # Location, Driver
`-- services/
    `-- matching.py # RideMatcher
```

## Trade-offs

- Distance is Manhattan (L1); replace with Haversine for real GPS coordinates.
- The snapshot is taken under no lock; a driver that goes unavailable between snapshot and lock acquisition is caught by the version check, not a pre-scan.
- Max-retry limit is not enforced; add a `max_retries` parameter to bound worst-case latency when all drivers are contested.

## Run

From this directory:

```bash
python3 app.py
```
