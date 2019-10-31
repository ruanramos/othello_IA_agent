# Internal
import typing as T

if T.TYPE_CHECKING:
    # Project
    from ...enums import Color
    from ...models import Board, Position
    from ...protocol import ViewProtocol


class HumanPlayer:
    def __init__(self, color: "Color") -> None:
        self.color = color

    def play(self, board: "Board", view: "ViewProtocol") -> "Position":
        while True:
            row_inp = int(input("Linha"))
            col_inp = int(input("Coluna"))
            move = Position(row_inp, col_inp)

            if move in board.valid_moves(self.color):
                break

            view.alert("Movimento invalido. Insira um válido")

        return move


__all__ = ("HumanPlayer",)
