from __future__ import annotations

from dataclasses import dataclass, field

from models.move import Move
from models.player import Player
from services.game_board import GameBoard


@dataclass(slots=True)
class TicTacToeGame:
    size: int
    players: list[Player]
    board: GameBoard = field(init=False)
    row_totals: list[int] = field(init=False)
    column_totals: list[int] = field(init=False)
    diagonal_total: int = field(default=0, init=False)
    anti_diagonal_total: int = field(default=0, init=False)
    current_turn_index: int = field(default=0, init=False)
    total_moves: int = field(default=0, init=False)
    winner_id: str | None = field(default=None, init=False)
    _players_by_id: dict[str, Player] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.size <= 0:
            raise ValueError("Board size must be positive")
        if len(self.players) != 2:
            raise ValueError("This implementation expects exactly two players")

        self.board = GameBoard(size=self.size)
        self.row_totals = [0] * self.size
        self.column_totals = [0] * self.size
        self._players_by_id = {player.player_id: player for player in self.players}

    def play_move(self, row: int, column: int, player_id: str) -> str:
        if self.winner_id is not None:
            raise ValueError("Game is already over")

        current_player = self.players[self.current_turn_index]
        if player_id != current_player.player_id:
            raise ValueError(f"It is {current_player.player_id}'s turn")

        move = Move(row=row, column=column, player_id=player_id)
        player = self._players_by_id[player_id]
        self.board.place(move.row, move.column, player.symbol)
        self._update_counters(move, player.weight)
        self.total_moves += 1

        if self._has_won(move):
            self.winner_id = player_id
            return f"{player_id} wins"

        if self.total_moves == self.size * self.size:
            return "Draw"

        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)
        return f"Move accepted for {player_id}"

    def render(self) -> list[str]:
        return self.board.render()

    def _update_counters(self, move: Move, weight: int) -> None:
        self.row_totals[move.row] += weight
        self.column_totals[move.column] += weight
        if move.row == move.column:
            self.diagonal_total += weight
        if move.row + move.column == self.size - 1:
            self.anti_diagonal_total += weight

    def _has_won(self, move: Move) -> bool:
        target = self.size
        return any(
            abs(total) == target
            for total in (
                self.row_totals[move.row],
                self.column_totals[move.column],
                self.diagonal_total,
                self.anti_diagonal_total,
            )
        )