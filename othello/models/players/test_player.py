# Internal

import math
import typing as T

# Project
if T.TYPE_CHECKING:
    from ...enums import Color
    from ...models import Board, Position

MAX_DEPTH = 4


def minimax(
        board: "Board", depth: int, color: "Color", maximizing: bool,
        heuristic: T.Callable[["Board", "Color"], float]) -> (float, "Position"):

    pos_to_play = (-1, -1)

    if depth == MAX_DEPTH:
        res = heuristic(board, color)
        return res, pos_to_play

    if maximizing:
        max_evaluation = -math.inf
        for child_board, pos in children_boards(board, color):
            (evaluation, _) = minimax(child_board, depth + 1, color.opposite(),
                                 not maximizing, heuristic)

            if max_evaluation < evaluation:
                max_evaluation = evaluation
                pos_to_play = pos

        return max_evaluation, pos_to_play

    else:
        min_evaluation = math.inf
        for child_board, pos in children_boards(board, color):
            (evaluation, _) = minimax(child_board, depth + 1, color.opposite(), not maximizing, heuristic)

            if min_evaluation > evaluation:
                min_evaluation = evaluation
                pos_to_play = pos

        return min_evaluation, pos_to_play


def children_boards(board: "Board", color: "Color") -> T.Sequence[T.Tuple["Board", "Position"]]:
    res = []
    valid_moves = list(board.valid_moves(color))
    for move in valid_moves:
        b = board.get_clone()
        b.play(move, color)
        res.append((b, move))

    return res


def get_a_child_board(board: "Board", color: "Color", valid_moves):
    b = board.get_clone()
    b.play(valid_moves.pop(0), color)
    return b


class TestPlayer:
    @staticmethod
    def num_of_coins_heuristic(board: "Board", color: "Color") -> float:
        actual_score = board.score()
        return 100 * (max(actual_score) - min(actual_score)) / (max(actual_score) - min(actual_score))

    def stupid(self, board: "Board", color: "Color") -> float:
        if self.color == '@':
            s = board.score()
            return s[1]
            # return board.score()[1]
        s = board.score()
        return s[0]

    def __init__(self, color: "Color") -> None:
        self.color = color

    def play(self, board: "Board") -> "Position":
        res = minimax(board, 0, self.color, True, self.stupid)
        return res[1]


__all__ = ("TestPlayer",)
