from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, timedelta


class PricingStrategy(ABC):
    @abstractmethod
    def quote(self, nightly_rate_cents: int, start_date: date, end_date: date) -> int:
        raise NotImplementedError


@dataclass(slots=True)
class WeekendHolidaySurgeStrategy(PricingStrategy):
    holiday_dates: set[date] = field(default_factory=set)

    def quote(self, nightly_rate_cents: int, start_date: date, end_date: date) -> int:
        total_nights = (end_date - start_date).days + 1
        base = nightly_rate_cents * total_nights
        if self._has_surge_day(start_date, end_date):
            return int(base * 1.2)
        return base

    def _has_surge_day(self, start_date: date, end_date: date) -> bool:
        current = start_date
        while current <= end_date:
            if current.weekday() >= 5 or current in self.holiday_dates:
                return True
            current += timedelta(days=1)
        return False