from models.move import ChessMove
from models.piece import Piece, PieceColor, PieceType
from models.position import Position
from services.chess_game import ChessGame


def main() -> None:
    game = ChessGame()
    game.board.place_piece(Position.from_algebraic("a1"), Piece(PieceType.ROOK, PieceColor.WHITE))
    game.board.place_piece(Position.from_algebraic("a4"), Piece(PieceType.BISHOP, PieceColor.BLACK))

    print(game.render())
    print(game.make_move(ChessMove(Position.from_algebraic("a1"), Position.from_algebraic("a4"))))
    print(game.render())
    print(game.undo())
    print(game.render())
    print(game.redo())
    print(game.render())


if __name__ == "__main__":
    main()