from __future__ import annotations

import threading
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Location:
    x: int
    y: int

    def distance_to(self, other: "Location") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass(slots=True)
class Driver:
    driver_id: str
    location: Location
    available: bool = True
    version: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)