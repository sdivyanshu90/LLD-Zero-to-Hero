from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Move:
    row: int
    column: int
    player_id: str