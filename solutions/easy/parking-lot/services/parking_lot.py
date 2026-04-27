from __future__ import annotations

from dataclasses import dataclass, field

from models.parking_spot import SpotCluster
from models.vehicle import Vehicle


@dataclass(slots=True)
class ParkingLot:
    cluster_count: int
    clusters: list[SpotCluster] = field(init=False)
    _vehicle_index: dict[str, SpotCluster] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        self.clusters = [SpotCluster(cluster_id=f"C{number}") for number in range(1, self.cluster_count + 1)]

    def park_vehicle(self, vehicle: Vehicle) -> str:
        if vehicle.license_plate in self._vehicle_index:
            raise ValueError(f"Vehicle {vehicle.license_plate} is already parked")

        for cluster in self.clusters:
            if cluster.can_fit(vehicle):
                location = cluster.park(vehicle)
                self._vehicle_index[vehicle.license_plate] = cluster
                return location

        raise ValueError(f"No space available for {vehicle.vehicle_type.value}")

    def release_vehicle(self, license_plate: str) -> str:
        cluster = self._vehicle_index.pop(license_plate, None)
        if cluster is None:
            raise ValueError(f"Vehicle {license_plate} is not parked")

        return cluster.release(license_plate)

    def snapshot(self) -> list[str]:
        return [cluster.describe() for cluster in self.clusters]