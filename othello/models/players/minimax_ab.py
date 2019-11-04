# Internal
import random
import math
import typing as T

# Project
if T.TYPE_CHECKING:
    from ...enums import Color
    from ...models import Board, Position

MAX_DEPTH = 3


def minimax(
        board: "Board", depth: int, color: "Color", maximizing: bool,
        alpha: float, beta: float,
        heuristic: T.Callable[["Board", "Color"], float]) -> (float, "Position"):

    pos_to_play = (-1, -1)

    if depth == MAX_DEPTH:
        res = heuristic(board, color)
        return res, pos_to_play

    if maximizing:
        max_evaluation = -math.inf
        for child_board, pos in children_boards(board, color):
            (evaluation, _) = minimax(child_board, depth + 1, color.opposite(),
                                 not maximizing, alpha, beta, heuristic)

            if max_evaluation < evaluation:
                max_evaluation = evaluation
                pos_to_play = pos
            alpha = max(alpha, evaluation)
            if (beta <= alpha):
                break
        return max_evaluation, pos_to_play

    else:
        min_evaluation = math.inf
        for child_board, pos in children_boards(board, color):
            (evaluation, _) = minimax(child_board, depth + 1, color.opposite(), 
            not maximizing, alpha, beta, heuristic)

            if min_evaluation > evaluation:
                min_evaluation = evaluation
                pos_to_play = pos
            beta = min(beta, evaluation)
            if (beta <= alpha):
                break
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


class MiniMaxAB:
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

    def simple_mobility(self, board: "Board", color: "Color") -> float:
        return len(board.valid_moves(color)) - len(board.valid_moves(color.opposite()))

    def frontier_control(self, board: "Board", color: "Color") -> float:
        def frontier(board: "Board"):
            def adjacent(px: int, py: int):
                r = []
                for i in range(-1, 1):
                    for j in range(-1, 1):
                        if (i == 0 and j == 0):
                            continue
                        x = px + i
                        y = py + j
                        if x > 0 and x < 9 and y > 0 and y < 9:
                            r.append((x, y))
            r = []
            for x, y in board.positions():
                if (x == 1 or y == 1 or x == 8 or y == 8):
                    continue
                for a in adjacent(x, y):
                    if board.get_square_color(a) == Color.EMPTY:
                        r.append(a)
                        break
            return r

        score = 0
        for p in frontier(board):
            pcolor = board.get_square_color(p[1], p[2])
            if pcolor == color:
                score -= 1
            elif pcolor == color.opposite:
                score += 1

        return score

        
            

    def __init__(self, color: "Color") -> None:
        self.color = color

    def play(self, board: "Board") -> "Position":
        res = minimax(board, 0, self.color, True, -math.inf, math.inf, self.frontier_control)
        return res[1]


__all__ = ("MiniMaxAB",)
