from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class RentalBooking:
    booking_id: str
    car_id: str
    start_date: date
    end_date: date

    def overlaps(self, other_start: date, other_end: date) -> bool:
        return not (self.end_date < other_start or other_end < self.start_date)