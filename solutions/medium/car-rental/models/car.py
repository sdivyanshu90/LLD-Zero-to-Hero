from dataclasses import dataclass, field
from datetime import date

from .booking import RentalBooking


@dataclass(slots=True)
class Car:
    car_id: str
    model: str
    bookings: list[RentalBooking] = field(default_factory=list)

    def is_available(self, start_date: date, end_date: date) -> bool:
        return all(not booking.overlaps(start_date, end_date) for booking in self.bookings)

    def reserve(self, booking_id: str, start_date: date, end_date: date) -> RentalBooking:
        if start_date > end_date:
            raise ValueError("Start date must be on or before end date")
        if not self.is_available(start_date, end_date):
            raise ValueError(f"Car {self.car_id} is not available for the requested range")
        booking = RentalBooking(booking_id=booking_id, car_id=self.car_id, start_date=start_date, end_date=end_date)
        self.bookings.append(booking)
        return booking