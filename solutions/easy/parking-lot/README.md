# Parking Lot Solution

This reference implementation models the core rule directly: each `SpotCluster` owns two adjacent car-sized spots and can behave either as one merged truck-capable unit or two split car slots.

## Design Notes

- `Vehicle` is an immutable value object.
- `ParkingSpot` models a single car-sized slot.
- `SpotCluster` encapsulates the split/merge lifecycle.
- `ParkingLot` handles allocation across clusters and prevents duplicate parking.

The merge rule is derived from state instead of toggled manually:

- If both child spots are empty and no truck is parked, the cluster is considered merged.
- If one or two cars occupy the child spots, the cluster is split.
- If a truck is parked, the whole cluster is occupied.

## Complexity Analysis

| Operation           | Time                              | Space                                      |
| ------------------- | --------------------------------- | ------------------------------------------ |
| `park_vehicle()`    | O(c) where c = number of clusters | O(1) extra                                 |
| `release_vehicle()` | O(1) via `_vehicle_index` dict    | O(1)                                       |
| `snapshot()`        | O(c)                              | O(c)                                       |
| Space (total)       | —                                 | O(c) for clusters + O(v) for vehicle index |

## SOLID Compliance

| Principle | Evidence                                                                                                                                        |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **SRP**   | `ParkingSpot` holds only occupancy state. `SpotCluster` owns the split/merge rule. `ParkingLot` handles allocation and the license-plate index. |
| **OCP**   | Adding a motorcycle type requires a new `VehicleType` enum value and a new `can_fit()` branch in `SpotCluster`. `ParkingLot` is unchanged.      |
| **LSP**   | All vehicles are passed through `park_vehicle(vehicle: Vehicle)`. No method downcasts to a concrete vehicle subtype.                            |
| **ISP**   | `ParkingLot`'s public interface is three methods. Internal helpers are private.                                                                 |
| **DIP**   | `ParkingLot` iterates `SpotCluster` objects by their `can_fit()` and `park()` contract, not by implementation details.                          |

## Folder Layout

```text
parking-lot/
|-- app.py
|-- models/
|   |-- __init__.py
|   |-- parking_spot.py
|   `-- vehicle.py
`-- services/
    |-- __init__.py
    `-- parking_lot.py
```

## Run

From this directory:

```bash
python app.py
```

The demo parks cars, shows the split state, releases cars, and then parks a truck once the cluster has automatically re-merged.
