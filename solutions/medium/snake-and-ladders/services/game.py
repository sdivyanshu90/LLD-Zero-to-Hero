from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from models.board import Board
from models.player import Player
from services.dice import DiceStrategy


@dataclass(slots=True)
class SnakeLadderGame:
    board: Board
    players: list[Player]
    dice: DiceStrategy
    _turns: deque[Player] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._turns = deque(self.players)

    def take_turn(self) -> str:
        player = self._turns.popleft()
        roll = self.dice.roll()
        attempted = player.position + roll
        if attempted <= self.board.size:
            player.position = self.board.resolve(attempted)
        self._turns.append(player)
        return f"{player.player_id} rolled {roll} and moved to {player.position}"

    def snapshot(self) -> dict[str, int]:
        return {player.player_id: player.position for player in self.players}