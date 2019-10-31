# Internal
import math
import typing as T

if T.TYPE_CHECKING:
    # Project
    from ...enums import Color
    from ...models import Board, Position


class CornerPlayer:
    @staticmethod
    def get_nearest_corner(moves: T.Sequence["Position"]) -> "Position":
        corners = [[1, 1], [1, 8], [8, 1], [8, 8]]
        min_dist = 10.0
        ret_move = moves[0]
        for move in moves:
            for corner in corners:
                dist = math.sqrt(abs(corner[0] - move.x) ** 2 + abs(corner[1] - move.y) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    ret_move = move

        return ret_move

    def __init__(self, color: "Color") -> None:
        self.color = color

    def play(self, board: "Board") -> "Position":
        return self.get_nearest_corner(board.valid_moves(self.color))


__all__ = ("CornerPlayer",)
