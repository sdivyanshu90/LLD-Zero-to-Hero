from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FloorRequest:
    floor: int