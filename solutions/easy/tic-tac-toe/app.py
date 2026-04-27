from models.player import Player
from services.tic_tac_toe import TicTacToeGame


def main() -> None:
    players = [Player(player_id="P1", symbol="X", weight=1), Player(player_id="P2", symbol="O", weight=-1)]
    game = TicTacToeGame(size=3, players=players)

    print(game.play_move(0, 0, "P1"))
    print(game.play_move(1, 0, "P2"))
    print(game.play_move(0, 1, "P1"))
    print(game.play_move(1, 1, "P2"))
    print(game.play_move(0, 2, "P1"))
    print(game.render())


if __name__ == "__main__":
    main()