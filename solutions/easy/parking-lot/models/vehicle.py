from dataclasses import dataclass
from enum import Enum


class VehicleType(Enum):
    CAR = "car"
    TRUCK = "truck"


@dataclass(frozen=True, slots=True)
class Vehicle:
    license_plate: str
    vehicle_type: VehicleType