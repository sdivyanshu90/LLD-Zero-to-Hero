from dataclasses import dataclass

from .position import Position


@dataclass(frozen=True, slots=True)
class ChessMove:
    from_position: Position
    to_position: Position