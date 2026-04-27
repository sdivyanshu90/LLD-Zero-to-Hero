import threading

from models.core import Driver, Location
from services.matching import RideMatcher


def main() -> None:
    matcher = RideMatcher(
        drivers=[
            Driver(driver_id="D1", location=Location(0, 0)),
            Driver(driver_id="D2", location=Location(3, 3)),
        ]
    )

    results: list[str | None] = []

    def request() -> None:
        results.append(matcher.request_ride(Location(1, 1)))

    threads = [threading.Thread(target=request), threading.Thread(target=request)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print(sorted(result for result in results if result is not None))
    print(matcher.snapshot())


if __name__ == "__main__":
    main()