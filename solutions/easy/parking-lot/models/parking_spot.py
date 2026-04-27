from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .vehicle import Vehicle, VehicleType


@dataclass(slots=True)
class ParkingSpot:
    spot_id: str
    occupied_by: Optional[Vehicle] = None

    @property
    def is_available(self) -> bool:
        return self.occupied_by is None


@dataclass(slots=True)
class SpotCluster:
    cluster_id: str
    truck_vehicle: Optional[Vehicle] = None
    left_spot: ParkingSpot = field(init=False)
    right_spot: ParkingSpot = field(init=False)

    def __post_init__(self) -> None:
        self.left_spot = ParkingSpot(f"{self.cluster_id}-L")
        self.right_spot = ParkingSpot(f"{self.cluster_id}-R")

    @property
    def is_merged(self) -> bool:
        return (
            self.truck_vehicle is None
            and self.left_spot.is_available
            and self.right_spot.is_available
        )

    def can_fit(self, vehicle: Vehicle) -> bool:
        if vehicle.vehicle_type is VehicleType.TRUCK:
            return self.is_merged

        return self.truck_vehicle is None and (
            self.left_spot.is_available or self.right_spot.is_available
        )

    def park(self, vehicle: Vehicle) -> str:
        if not self.can_fit(vehicle):
            raise ValueError(f"Cluster {self.cluster_id} cannot fit {vehicle.vehicle_type.value}")

        if vehicle.vehicle_type is VehicleType.TRUCK:
            self.truck_vehicle = vehicle
            return self.cluster_id

        if self.left_spot.is_available:
            self.left_spot.occupied_by = vehicle
            return self.left_spot.spot_id

        self.right_spot.occupied_by = vehicle
        return self.right_spot.spot_id

    def release(self, license_plate: str) -> str:
        if self.truck_vehicle and self.truck_vehicle.license_plate == license_plate:
            self.truck_vehicle = None
            return self.cluster_id

        for spot in (self.left_spot, self.right_spot):
            vehicle = spot.occupied_by
            if vehicle and vehicle.license_plate == license_plate:
                spot.occupied_by = None
                return spot.spot_id

        raise ValueError(f"Vehicle {license_plate} is not parked in cluster {self.cluster_id}")

    def describe(self) -> str:
        if self.truck_vehicle is not None:
            return f"{self.cluster_id}: truck={self.truck_vehicle.license_plate}"

        if self.is_merged:
            return f"{self.cluster_id}: merged-empty"

        left_label = self.left_spot.occupied_by.license_plate if self.left_spot.occupied_by else "empty"
        right_label = self.right_spot.occupied_by.license_plate if self.right_spot.occupied_by else "empty"
        return f"{self.cluster_id}: split [{left_label} | {right_label}]"