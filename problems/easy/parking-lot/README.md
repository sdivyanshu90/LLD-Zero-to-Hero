# Parking Lot

## Problem Summary

Design a parking lot that supports cars and trucks.

- A car occupies one car-sized slot.
- A truck occupies two adjacent car-sized slots.
- If a truck-sized area is split into two car slots, those slots must merge back into a truck-sized area once both car slots become free again.

This problem is intentionally small, but it tests whether the design models real ownership and lifecycle rules instead of hiding them in a few `if` statements.

## Why This Problem Is Asked

Interviewers use this to verify that candidates can identify _who owns a rule_ rather than reaching for flags and index arithmetic. The split/merge lifecycle is the crux: a candidate who puts that logic in `ParkingLot` produces a fragile design, whereas one who isolates it in `SpotCluster` demonstrates genuine SRP thinking.

This problem also scales well — adding floors, electric chargers, or reservations can expose whether the design is truly extensible or secretly brittle.

## Functional Requirements

1. Park a car in a single available car slot.
2. Park a truck only when two adjacent free car slots are available as one merged unit.
3. Remove a parked vehicle by its identifier.
4. Re-merge two adjacent car slots into one truck-capable unit when both halves are empty.
5. Expose the current parking-lot state for debugging or display.

## Constraints

- Do not use multithreading for this version.
- Keep the model object-oriented; avoid turning the solution into raw arrays plus helper functions.
- Favor small classes with single responsibilities.
- The design should make the split-vs-merged state explicit.

## ASCII UML

```text
+-------------------+     +-------------------+
| Vehicle           |     | ParkingSpot       |
+-------------------+     +-------------------+
| plate             |     | spot_id           |
| vehicle_type      |     | occupant          |
+-------------------+     +-------------------+

+-------------------+     +-------------------+
| SpotCluster       |<>-->| ParkingSpot x2    |
+-------------------+     +-------------------+
| cluster_id        |
| truck_occupant    |
+-------------------+
| is_truck_ready()  |
| park_truck()      |
| park_car()        |
| release()         |
+-------------------+

+-------------------+
| ParkingLot        |
+-------------------+
| clusters          |
| allocations       |
+-------------------+
| park()            |
| remove()          |
| snapshot()        |
+-------------------+
```

## SOLID Principles in Play

| Principle | How It Applies                                                                                                             |
| --------- | -------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `SpotCluster` owns the split/merge rule. `ParkingLot` owns allocation only. `ParkingSpot` is pure state.                   |
| **OCP**   | Adding motorcycles means a new vehicle type and a new `can_fit()` check in `SpotCluster` — zero changes to `ParkingLot`.   |
| **LSP**   | All vehicle types go through the same `park_vehicle()` call; the polymorphism lives in `SpotCluster.can_fit()`.            |
| **ISP**   | `Vehicle` carries only identity; it does not know anything about parking mechanics.                                        |
| **DIP**   | `ParkingLot` iterates over `SpotCluster` objects via their public contract, not their concrete split/merge implementation. |

## Key Edge Cases

- Parking a truck when only one car slot in a pair is free must fail.
- Removing one car from a split pair must not merge the pair if the other half is still occupied.
- Removing the second car from a split pair must automatically restore truck capacity.
- Parking the same vehicle twice should be rejected.
- Removing a vehicle that is not present should be rejected.

## Suggested Domain Model

- `Vehicle`: common information such as license plate and type.
- `ParkingSpot`: one physical car-sized slot.
- `SpotCluster`: two adjacent car-sized slots that can behave either as:
  - one merged truck-capable unit, or
  - two split car slots.
- `ParkingLot`: coordination layer that finds space and tracks active allocations.

The important design decision is not "how do I find an index in a list?". It is "what object owns the split/merge rule?". A good answer keeps that rule close to the `SpotCluster` instead of scattering it across controllers.

## What Interviewers Usually Look For

- Clear separation between domain objects and orchestration.
- Correct handling of the split/merge lifecycle.
- Readable naming and small methods.
- A solution that can later extend to motorcycles, floors, payment, or pricing without rewriting everything.

## Follow-up Questions

1. How would you add motorcycles that can share special compact spots?
2. How would you support multiple floors?
3. How would you reserve spots ahead of time?
4. What changes if the lot becomes concurrent?
