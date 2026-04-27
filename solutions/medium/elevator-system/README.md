# Elevator System Solution

This implementation uses LOOK-style sweeps: keep serving requests in the current direction while work exists ahead, then reverse only when that directional queue is exhausted.

## Design Notes

- `FloorRequest` models one stop request.
- `ElevatorController` owns current floor, direction, and pending stops.
- The controller keeps separate upward and downward stop sets.

## Complexity Analysis

| Operation              | Time                                          | Space                           |
| ---------------------- | --------------------------------------------- | ------------------------------- |
| `add_request(request)` | O(1) set insert                               | O(1)                            |
| `step()`               | O(p), p = pending stops in current direction  | O(1)                            |
| `run_until_idle()`     | O(p × log p) total (min/max of set each step) | O(p) path                       |
| Space (total)          | —                                             | O(r) where r = pending requests |

Using a `SortedList` instead of a plain set would reduce each `step()` to O(log p).

## SOLID Compliance

| Principle | Evidence                                                                                                                                                     |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **SRP**   | `FloorRequest` is a data class. `ElevatorController` owns directional sweep logic. Neither bleeds into the other.                                            |
| **OCP**   | Adding emergency priority means a new field on `FloorRequest` and a modified comparator in `_next_floor()` — the core sweep logic is structurally unchanged. |
| **LSP**   | Any `FloorRequest` subtype (floor button, app request) can be added without changing the controller.                                                         |
| **ISP**   | `ElevatorController` exposes `add_request()`, `step()`, and `run_until_idle()`. Internal direction-reversal helpers are private.                             |
| **DIP**   | `ElevatorController` processes `FloorRequest` data objects; it is not coupled to any specific requester component.                                           |

## Design Pattern

LOOK sweep algorithm: two `SortedList` (or `sorted set`) structures hold pending up-stops and down-stops. `step()` always moves toward the nearest stop in the current direction; only reverses when the directional queue is exhausted. This mirrors the disk-scheduling LOOK algorithm.

## Folder Layout

```text
elevator-system/
|-- app.py
|-- models/
|   |-- direction.py
|   `-- request.py
`-- services/
    `-- elevator_controller.py
```

## Trade-offs

- Single elevator; extend with a `Dispatcher` that picks the nearest idle elevator for multi-elevator scenarios.
- Stop deduplication is handled by using a `set`; repeated calls for the same floor are silently ignored.

## Run

From this directory:

```bash
python app.py
```
