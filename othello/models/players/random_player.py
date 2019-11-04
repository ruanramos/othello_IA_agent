# Internal
import random
import typing as T

if T.TYPE_CHECKING:
    # Project
    from ...enums import Color
    from ...models import Board, Position


class RandomPlayer:
    def __init__(self, color: "Color") -> None:
        self.color = color

    def play(self, board: "Board") -> "Position":
        print("Possible Moves for color {}: {}".format(self.color, board.valid_moves(self.color)))
        print("-----------------------------")
        return random.choice(board.valid_moves(self.color))


__all__ = ("RandomPlayer",)
