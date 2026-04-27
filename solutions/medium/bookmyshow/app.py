import time

from models.seat import Seat
from services.booking_service import BookingService


def main() -> None:
    service = BookingService(seats=[Seat("A1"), Seat("A2")], lock_duration_seconds=0.1, sweep_interval_seconds=0.02)
    try:
        print(service.lock_seat("A1", "user-1"))
        print(service.snapshot())
        time.sleep(0.15)
        print(service.snapshot())
        print(service.lock_seat("A1", "user-2"))
        print(service.confirm_booking("A1", "user-2"))
        print(service.snapshot())
    finally:
        service.shutdown()


if __name__ == "__main__":
    main()