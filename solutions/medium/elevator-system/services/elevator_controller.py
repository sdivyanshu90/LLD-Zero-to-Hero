from __future__ import annotations

from dataclasses import dataclass, field

from models.direction import Direction
from models.request import FloorRequest


@dataclass(slots=True)
class ElevatorController:
    current_floor: int
    direction: Direction = Direction.IDLE
    up_stops: set[int] = field(default_factory=set)
    down_stops: set[int] = field(default_factory=set)
    visited_floors: list[int] = field(default_factory=list)

    def add_request(self, request: FloorRequest) -> None:
        if request.floor == self.current_floor:
            return

        if request.floor > self.current_floor:
            self.up_stops.add(request.floor)
        else:
            self.down_stops.add(request.floor)

        if self.direction is Direction.IDLE:
            self.direction = Direction.UP if self.up_stops else Direction.DOWN

    def step(self) -> int | None:
        next_floor = self._next_floor()
        if next_floor is None:
            self.direction = Direction.IDLE
            return None

        self.current_floor = next_floor
        self.visited_floors.append(next_floor)
        self.up_stops.discard(next_floor)
        self.down_stops.discard(next_floor)

        if not self._has_pending_in_direction(self.direction):
            self._reverse_if_needed()

        return next_floor

    def run_until_idle(self) -> list[int]:
        path: list[int] = []
        while True:
            next_floor = self.step()
            if next_floor is None:
                return path
            path.append(next_floor)

    def snapshot(self) -> dict[str, object]:
        return {
            "current_floor": self.current_floor,
            "direction": self.direction.value,
            "up_stops": sorted(self.up_stops),
            "down_stops": sorted(self.down_stops, reverse=True),
            "visited_floors": list(self.visited_floors),
        }

    def _next_floor(self) -> int | None:
        if self.direction is Direction.UP:
            ahead = [floor for floor in self.up_stops if floor >= self.current_floor]
            if ahead:
                return min(ahead)
            if self.down_stops:
                self.direction = Direction.DOWN
                return max(self.down_stops)
            return None

        if self.direction is Direction.DOWN:
            below = [floor for floor in self.down_stops if floor <= self.current_floor]
            if below:
                return max(below)
            if self.up_stops:
                self.direction = Direction.UP
                return min(self.up_stops)
            return None

        if self.up_stops:
            self.direction = Direction.UP
            return min(self.up_stops)
        if self.down_stops:
            self.direction = Direction.DOWN
            return max(self.down_stops)
        return None

    def _has_pending_in_direction(self, direction: Direction) -> bool:
        if direction is Direction.UP:
            return any(floor > self.current_floor for floor in self.up_stops)
        if direction is Direction.DOWN:
            return any(floor < self.current_floor for floor in self.down_stops)
        return False

    def _reverse_if_needed(self) -> None:
        if self.direction is Direction.UP and self.down_stops:
            self.direction = Direction.DOWN
        elif self.direction is Direction.DOWN and self.up_stops:
            self.direction = Direction.UP
        elif not self.up_stops and not self.down_stops:
            self.direction = Direction.IDLE