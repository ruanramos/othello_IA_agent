# Internal
import typing as T
from itertools import product
from collections import defaultdict

# Project
from ..enums import Color
from .position import Position

# Basic directions
UP, DOWN, LEFT, RIGHT = Position(-1, 0), Position(1, 0), Position(0, -1), Position(0, 1)

BoardState_t = T.MutableMapping[T.Tuple[int, int], Color]


class Board:
    # Maintain compatibility with old version
    EMPTY, BLACK, WHITE, OUTER = Color  # type: ignore  # mypy issue #2305

    DIRECTIONS = UP, DOWN, LEFT, RIGHT, UP + LEFT, UP + RIGHT, DOWN + LEFT, DOWN + RIGHT

    @staticmethod
    def positions() -> T.Iterator[T.Tuple[int, int]]:
        return product(range(1, 9), repeat=2)  # type: ignore # typeshed is too generic here

    def __init__(self, board: T.Optional[BoardState_t]) -> None:
        self._board: BoardState_t = defaultdict(lambda: Color.OUTER)

        if board is None:
            for i, j in self.positions():
                self[i, j] = Color.EMPTY

            self[4, 4], self[4, 5] = Color.WHITE, Color.BLACK
            self[5, 4], self[5, 5] = Color.BLACK, Color.WHITE
        else:
            self._board.update(board.items())

    def __iter__(self) -> T.Iterator[T.Tuple[Color, ...]]:
        for i in range(0, 10):
            yield self[i]

    @T.overload
    def __getitem__(self, item: int) -> T.Tuple[Color, ...]:
        ...

    @T.overload
    def __getitem__(self, item: T.Tuple[int, int]) -> Color:
        ...

    def __getitem__(
        self, item: T.Union[int, T.Tuple[int, int]]
    ) -> T.Union[T.Tuple[Color, ...], Color]:
        if isinstance(item, int):
            return tuple(self[item, j] for j in range(0, 10))

        return self._board[item]

    def __setitem__(self, item: T.Tuple[int, int], value: Color) -> None:
        self._board[item] = value

    def play(self, move: T.Tuple[int, int], color: Color) -> None:
        assert color == Color.BLACK or color == Color.WHITE

        self[move] = color

        for direction in Board.DIRECTIONS:
            self._make_flips(move, color, direction)

    @property
    def board(self) -> "Board":
        # Maintain compatibility with old version
        return self

    def score(self) -> T.Tuple[int, int]:
        white = sum(1 for i, j in self.positions() if self[i, j] == Color.WHITE)
        black = sum(1 for i, j in self.positions() if self[i, j] == Color.BLACK)
        return white, black

    def get_clone(self) -> "Board":
        return Board(self._board)

    def valid_moves(self, color: Color) -> T.Sequence[Position]:
        ret = []
        for i, j in self.positions():
            if self[i, j] == Color.EMPTY:
                for direction in Board.DIRECTIONS:
                    move = Position(i, j)
                    if self._find_bracket(move, color, direction):
                        ret.append(move)
        return tuple(ret)

    def _make_flips(self, move: T.Tuple[int, int], color: Color, direction: Position) -> None:
        bracket = self._find_bracket(move, color, direction)

        if not bracket:
            return

        # flips
        square_pos = direction + move
        while square_pos != bracket:
            self[square_pos] = color
            square_pos += direction

    def _find_bracket(
        self, move: T.Tuple[int, int], color: Color, direction: Position
    ) -> T.Optional[Position]:
        bracket_pos = direction + move
        bracket_color = self[bracket_pos]

        if bracket_color == color:
            return None

        opponent = color.opposite()
        while bracket_color == opponent:
            bracket_pos += direction
            bracket_color = self[bracket_pos]

        return None if bracket_color in (Color.OUTER, Color.EMPTY) else bracket_pos


__all__ = ("Board",)
