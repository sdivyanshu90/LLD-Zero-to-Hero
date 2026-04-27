from __future__ import annotations

from dataclasses import dataclass, field

from models.move import ChessMove
from models.piece import Piece
from services.chess_board import ChessBoard


@dataclass(slots=True)
class MoveCommand:
    board: ChessBoard
    move: ChessMove
    moved_piece: Piece | None = field(default=None, init=False)
    captured_piece: Piece | None = field(default=None, init=False)
    _executed: bool = field(default=False, init=False, repr=False)

    def execute(self) -> str:
        self.moved_piece, self.captured_piece = self.board.apply_move(self.move)
        self._executed = True
        if self.captured_piece is None:
            return "Move executed"
        return f"Move executed and captured {self.captured_piece.symbol()}"

    def undo(self) -> str:
        if not self._executed or self.moved_piece is None:
            raise ValueError("Cannot undo a move that was never executed")

        self.board.restore_move(self.move, self.moved_piece, self.captured_piece)
        self._executed = False
        if self.captured_piece is None:
            return "Move undone"
        return f"Move undone and restored {self.captured_piece.symbol()}"