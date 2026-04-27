from __future__ import annotations

from dataclasses import dataclass, field

from models.move import ChessMove
from models.piece import Piece
from models.position import Position


@dataclass(slots=True)
class ChessBoard:
    pieces_by_position: dict[Position, Piece] = field(default_factory=dict)

    def place_piece(self, position: Position, piece: Piece) -> None:
        self.pieces_by_position[position] = piece

    def piece_at(self, position: Position) -> Piece | None:
        return self.pieces_by_position.get(position)

    def apply_move(self, move: ChessMove) -> tuple[Piece, Piece | None]:
        piece = self.piece_at(move.from_position)
        if piece is None:
            raise ValueError("No piece exists at the source square")

        captured_piece = self.piece_at(move.to_position)
        self.pieces_by_position.pop(move.from_position)
        self.pieces_by_position[move.to_position] = piece
        return piece, captured_piece

    def restore_move(self, move: ChessMove, moved_piece: Piece, captured_piece: Piece | None) -> None:
        self.pieces_by_position.pop(move.to_position, None)
        self.pieces_by_position[move.from_position] = moved_piece
        if captured_piece is not None:
            self.pieces_by_position[move.to_position] = captured_piece

    def render(self) -> list[str]:
        rows: list[str] = []
        for row in range(7, -1, -1):
            cells: list[str] = []
            for column in range(8):
                piece = self.piece_at(Position(row=row, column=column))
                cells.append(piece.symbol() if piece else ".")
            rows.append(" ".join(cells))
        return rows