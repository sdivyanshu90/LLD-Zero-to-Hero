from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from models.room import Room
from services.pricing import PricingStrategy


@dataclass(slots=True)
class HotelBookingService:
    pricing_strategy: PricingStrategy
    rooms: dict[str, Room] = field(default_factory=dict)

    def add_room(self, room: Room) -> None:
        self.rooms[room.room_id] = room

    def search_available(self, start_date: date, end_date: date) -> list[str]:
        return sorted(room_id for room_id, room in self.rooms.items() if room.is_available(start_date, end_date))

    def quote(self, room_id: str, start_date: date, end_date: date) -> int:
        room = self._get_room(room_id)
        return self.pricing_strategy.quote(room.nightly_rate_cents, start_date, end_date)

    def reserve(self, room_id: str, booking_id: str, start_date: date, end_date: date) -> str:
        room = self._get_room(room_id)
        room.reserve(booking_id, start_date, end_date)
        return f"Reserved {room_id} from {start_date.isoformat()} to {end_date.isoformat()}"

    def _get_room(self, room_id: str) -> Room:
        room = self.rooms.get(room_id)
        if room is None:
            raise ValueError(f"Unknown room {room_id}")
        return room