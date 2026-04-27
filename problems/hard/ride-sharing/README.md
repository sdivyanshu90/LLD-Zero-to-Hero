# Ride-Sharing

## Problem Summary

Design a ride-matching service that finds nearby drivers and uses optimistic locking to prevent double-booking the same driver.

## Why This Problem Is Asked

Ride matching is a high-concurrency real-time assignment problem. The key insight is that the naive approach — find the nearest available driver, then mark them unavailable — has a TOCTOU race window between the distance sort and the assignment.

Optimistic concurrency control (OCC) via version fields is the correct answer: read the driver’s version before sorting, then acquire the driver’s lock and verify the version has not changed before committing the assignment. If another thread snuck in, skip this driver and try the next candidate.

## Functional Requirements

1. Register drivers with location coordinates and availability status.
2. Accept a ride request with an origin location.
3. Find the nearest available drivers within a search radius.
4. Use optimistic versioning to assign exactly one driver to a request.
5. Retry the assignment if a version conflict is detected; fail if no driver can be secured.

## ASCII UML

```text
+-------------------+
| Driver            |
+-------------------+
| driver_id         |
| location          |
| available         |
| version           |
+-------------------+

+-------------------+
| RideMatcher       |
+-------------------+
| drivers           |
+-------------------+
| request_ride()    |
| _try_assign()     |
+-------------------+
```

## Concurrency Checklist

- Shared state: driver availability and version fields.
- Deadlock risk: lock one driver at a time during optimistic commit.
- Lock granularity: per-driver locking is the right scope here.
- Lock-free alternative: versioned CAS on driver state in a lower-level runtime.

## SOLID Principles in Play

| Principle | How It Applies                                                                                                                                       |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `Driver` holds location, availability, and version. `RideMatcher` owns proximity sorting and optimistic assignment. `Location` is a pure value type. |
| **OCP**   | Adding a `VehicleTypeFilter` means a new pre-sort filter applied in `request_ride()`; the OCC assignment loop is unchanged.                          |
| **LSP**   | Any `Driver` subtype (car, bike, truck) satisfies the same availability and version interface; `RideMatcher` treats all uniformly.                   |
| **ISP**   | `RideMatcher` exposes only `request_ride()` and `snapshot()`. Internal OCC retry logic is hidden.                                                    |
| **DIP**   | `RideMatcher` accepts a list of `Driver` objects through their public interface; it does not depend on any ride-management service.                  |

## Key Edge Cases

- Two concurrent ride requests targeting the same nearest driver must result in at most one successful assignment.
- A request with no available drivers must fail with a clear error, not silently hang.
- Optimistic lock conflicts must trigger a retry before giving up entirely.

## Follow-up Questions

1. How would you add surge pricing based on the local driver-to-rider ratio?
2. How would you support ride pooling where one driver picks up multiple riders heading in the same direction?
3. How would you use geohashing to make the nearby-driver lookup more efficient at scale?
