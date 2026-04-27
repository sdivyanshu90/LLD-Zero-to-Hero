from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Player:
    player_id: str
    symbol: str
    weight: int