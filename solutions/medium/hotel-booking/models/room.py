from dataclasses import dataclass, field
from datetime import date

from .booking import HotelBooking


@dataclass(slots=True)
class Room:
    room_id: str
    nightly_rate_cents: int
    bookings: list[HotelBooking] = field(default_factory=list)

    def is_available(self, start_date: date, end_date: date) -> bool:
        return all(not booking.overlaps(start_date, end_date) for booking in self.bookings)

    def reserve(self, booking_id: str, start_date: date, end_date: date) -> HotelBooking:
        if start_date > end_date:
            raise ValueError("Start date must be on or before end date")
        if not self.is_available(start_date, end_date):
            raise ValueError(f"Room {self.room_id} is not available")
        booking = HotelBooking(booking_id=booking_id, room_id=self.room_id, start_date=start_date, end_date=end_date)
        self.bookings.append(booking)
        return booking