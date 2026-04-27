from datetime import date

from models.room import Room
from services.hotel_booking import HotelBookingService
from services.pricing import WeekendHolidaySurgeStrategy


def main() -> None:
    strategy = WeekendHolidaySurgeStrategy(holiday_dates={date(2026, 12, 25)})
    service = HotelBookingService(pricing_strategy=strategy)
    service.add_room(Room(room_id="R1", nightly_rate_cents=5000))
    service.add_room(Room(room_id="R2", nightly_rate_cents=8000))

    start = date(2026, 5, 1)
    end = date(2026, 5, 3)
    print(service.quote("R1", start, end))
    print(service.reserve("R1", "HB-1", start, end))
    print(service.search_available(start, end))


if __name__ == "__main__":
    main()