from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field

from models.seat import Seat, SeatStatus


@dataclass(slots=True)
class BookingService:
    seats: list[Seat]
    lock_duration_seconds: float = 600.0
    sweep_interval_seconds: float = 1.0
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)
    _stop_event: threading.Event = field(default_factory=threading.Event, init=False, repr=False)
    _cleaner_thread: threading.Thread = field(init=False, repr=False)
    _seats_by_id: dict[str, Seat] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._seats_by_id = {seat.seat_id: seat for seat in self.seats}
        self._cleaner_thread = threading.Thread(target=self._expire_loop, daemon=True)
        self._cleaner_thread.start()

    def lock_seat(self, seat_id: str, user_id: str) -> str:
        with self._lock:
            self._expire_locked_seats(time.monotonic())
            seat = self._get_seat(seat_id)
            if seat.status is not SeatStatus.AVAILABLE:
                raise ValueError(f"Seat {seat_id} is not available")
            seat.status = SeatStatus.LOCKED
            seat.locked_by = user_id
            seat.locked_until = time.monotonic() + self.lock_duration_seconds
            return f"Locked {seat_id} for {user_id}"

    def confirm_booking(self, seat_id: str, user_id: str) -> str:
        with self._lock:
            self._expire_locked_seats(time.monotonic())
            seat = self._get_seat(seat_id)
            if seat.status is not SeatStatus.LOCKED or seat.locked_by != user_id:
                raise ValueError(f"Seat {seat_id} is not locked by {user_id}")
            seat.status = SeatStatus.BOOKED
            seat.locked_until = None
            return f"Booked {seat_id} for {user_id}"

    def snapshot(self) -> dict[str, str]:
        with self._lock:
            self._expire_locked_seats(time.monotonic())
            return {seat_id: seat.status.value for seat_id, seat in sorted(self._seats_by_id.items())}

    def shutdown(self) -> None:
        self._stop_event.set()
        self._cleaner_thread.join(timeout=1)

    def _expire_loop(self) -> None:
        while not self._stop_event.wait(self.sweep_interval_seconds):
            with self._lock:
                self._expire_locked_seats(time.monotonic())

    def _expire_locked_seats(self, now: float) -> None:
        for seat in self._seats_by_id.values():
            if seat.status is SeatStatus.LOCKED and seat.locked_until is not None and seat.locked_until <= now:
                seat.status = SeatStatus.AVAILABLE
                seat.locked_by = None
                seat.locked_until = None

    def _get_seat(self, seat_id: str) -> Seat:
        seat = self._seats_by_id.get(seat_id)
        if seat is None:
            raise ValueError(f"Unknown seat {seat_id}")
        return seat