from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from models.car import Car


@dataclass(slots=True)
class CarRentalService:
    cars: dict[str, Car] = field(default_factory=dict)

    def add_car(self, car: Car) -> None:
        self.cars[car.car_id] = car

    def search_available(self, start_date: date, end_date: date) -> list[str]:
        return sorted(car_id for car_id, car in self.cars.items() if car.is_available(start_date, end_date))

    def reserve_car(self, car_id: str, booking_id: str, start_date: date, end_date: date) -> str:
        car = self.cars.get(car_id)
        if car is None:
            raise ValueError(f"Unknown car {car_id}")
        booking = car.reserve(booking_id, start_date, end_date)
        return f"Reserved {booking.car_id} for {booking.start_date.isoformat()} to {booking.end_date.isoformat()}"