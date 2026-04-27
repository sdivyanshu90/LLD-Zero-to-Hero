# Elevator System

## Problem Summary

Design a single-elevator controller that serves requests using SCAN or LOOK-style directional sweeps instead of FIFO.

The elevator should keep moving in one direction while requests still exist ahead of it, then reverse only when that directional work is exhausted.

## Why This Problem Is Asked

The SCAN / LOOK algorithm from disk scheduling maps directly to elevator controllers and is a favorite in systems-design interviews. It tests whether the candidate moves beyond FIFO and can explain why directional sweeps minimise average wait time.

The LOOK variant (reverse on last pending request in that direction, not at the floor limit) is often what interviewers expect. Candidates who implement pure FIFO or who cannot articulate the difference score lower on algorithm selection.

## Functional Requirements

1. Accept floor requests.
2. Track current floor and direction.
3. Serve requests in directional-sweep order.
4. Reverse direction only when the current sweep is finished.
5. Expose the service order for debugging.

## Constraints

- Never process requests purely in insertion order.
- Directional decision logic should live in the controller, not in the demo code.
- The implementation should make the distinction between upward and downward pending work explicit.

## ASCII UML

```text
+-------------------+
| FloorRequest      |
+-------------------+
| floor             |
+-------------------+

+-------------------+
| Direction         |
+-------------------+
| UP                |
| DOWN              |
| IDLE              |
+-------------------+

+-------------------+
| ElevatorController|
+-------------------+
| current_floor     |
| direction         |
| up_stops          |
| down_stops        |
+-------------------+
| add_request()     |
| step()            |
| run_until_idle()  |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                           |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `FloorRequest` is pure data. `ElevatorController` owns direction state, stop sets, and the step logic.                                   |
| **OCP**   | Adding emergency override is a new `RequestPriority` field on `FloorRequest`; the LOOK sweep logic can prioritize without restructuring. |
| **LSP**   | Any `FloorRequest` subtype (internal button, external call) can be added to the controller’s stop sets without changing the sweep logic. |
| **ISP**   | `ElevatorController` exposes only `add_request()`, `step()`, and `run_until_idle()`. Internal direction-reversal helpers are private.    |
| **DIP**   | `ElevatorController` processes `FloorRequest` data objects; it does not depend on a concrete requester (panel button, app, etc.).        |

## Key Edge Cases

- Requests for the current floor should not poison the queues.
- Reversing direction too early breaks the SCAN/LOOK guarantee.
- Duplicate requests should not create duplicate stops.

## Follow-up Questions

1. How would you handle multiple elevators?
2. How would you incorporate passenger direction on pickup?
3. How would you prioritize emergency or VIP requests?
