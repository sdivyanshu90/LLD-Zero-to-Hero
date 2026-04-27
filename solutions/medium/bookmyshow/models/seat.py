from dataclasses import dataclass
from enum import Enum


class SeatStatus(Enum):
    AVAILABLE = "available"
    LOCKED = "locked"
    BOOKED = "booked"


@dataclass(slots=True)
class Seat:
    seat_id: str
    status: SeatStatus = SeatStatus.AVAILABLE
    locked_by: str | None = None
    locked_until: float | None = None