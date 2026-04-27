from __future__ import annotations

from dataclasses import dataclass

from models.core import Driver, Location


@dataclass(slots=True)
class RideMatcher:
    drivers: list[Driver]

    def request_ride(self, pickup: Location) -> str | None:
        candidates = sorted(
            ((driver.location.distance_to(pickup), driver.version, driver) for driver in self.drivers if driver.available),
            key=lambda item: (item[0], item[2].driver_id),
        )
        for _, expected_version, driver in candidates:
            if self._try_assign(driver, expected_version):
                return driver.driver_id
        return None

    def snapshot(self) -> dict[str, tuple[bool, int]]:
        return {driver.driver_id: (driver.available, driver.version) for driver in self.drivers}

    def _try_assign(self, driver: Driver, expected_version: int) -> bool:
        with driver.lock:
            if not driver.available or driver.version != expected_version:
                return False
            driver.available = False
            driver.version += 1
            return True