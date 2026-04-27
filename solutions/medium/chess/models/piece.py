from dataclasses import dataclass
from enum import Enum


class PieceType(Enum):
    KING = "K"
    QUEEN = "Q"
    ROOK = "R"
    BISHOP = "B"
    KNIGHT = "N"
    PAWN = "P"


class PieceColor(Enum):
    WHITE = "white"
    BLACK = "black"


@dataclass(frozen=True, slots=True)
class Piece:
    piece_type: PieceType
    color: PieceColor

    def symbol(self) -> str:
        symbol = self.piece_type.value
        return symbol if self.color is PieceColor.WHITE else symbol.lower()