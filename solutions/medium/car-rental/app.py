from datetime import date

from models.car import Car
from services.car_rental import CarRentalService


def main() -> None:
    service = CarRentalService()
    service.add_car(Car(car_id="C1", model="Sedan"))
    service.add_car(Car(car_id="C2", model="SUV"))

    start = date(2026, 5, 1)
    end = date(2026, 5, 3)
    print(service.reserve_car("C1", "B1", start, end))
    print(service.search_available(start, end))
    print(service.search_available(date(2026, 5, 4), date(2026, 5, 6)))


if __name__ == "__main__":
    main()