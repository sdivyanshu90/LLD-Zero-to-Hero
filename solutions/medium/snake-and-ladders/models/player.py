from dataclasses import dataclass


@dataclass(slots=True)
class Player:
    player_id: str
    position: int = 0