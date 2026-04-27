from __future__ import annotations

from dataclasses import dataclass, field

from models.move import ChessMove
from services.chess_board import ChessBoard
from services.move_command import MoveCommand


@dataclass(slots=True)
class ChessGame:
    board: ChessBoard = field(default_factory=ChessBoard)
    undo_stack: list[MoveCommand] = field(default_factory=list)
    redo_stack: list[MoveCommand] = field(default_factory=list)

    def make_move(self, move: ChessMove) -> str:
        command = MoveCommand(board=self.board, move=move)
        message = command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()
        return message

    def undo(self) -> str:
        if not self.undo_stack:
            raise ValueError("No moves to undo")
        command = self.undo_stack.pop()
        message = command.undo()
        self.redo_stack.append(command)
        return message

    def redo(self) -> str:
        if not self.redo_stack:
            raise ValueError("No moves to redo")
        command = self.redo_stack.pop()
        message = command.execute()
        self.undo_stack.append(command)
        return message

    def render(self) -> list[str]:
        return self.board.render()