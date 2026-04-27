from models.board import Board
from models.player import Player
from services.dice import DeterministicDice
from services.game import SnakeLadderGame


def main() -> None:
    board = Board(size=30, jumps={3: 22, 27: 1, 11: 26})
    game = SnakeLadderGame(board=board, players=[Player("P1"), Player("P2")], dice=DeterministicDice([3, 4, 6, 2]))

    print(game.take_turn())
    print(game.take_turn())
    print(game.snapshot())


if __name__ == "__main__":
    main()