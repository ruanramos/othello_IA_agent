# Internal
import typing as T
from enum import Enum, unique


@unique
class Color(Enum):
    EMPTY = "."
    BLACK = "@"
    WHITE = "o"
    OUTER = "?"

    def __eq__(self, other: object) -> bool:
        ret: bool = self.value == other if isinstance(other, str) else super().__eq__(other)
        return ret

    def __hash__(self) -> int:
        ret: int = self.value.__hash__()
        return ret

    def opposite(self) -> "Color":
        if self in (Color.EMPTY, Color.OUTER):
            raise ValueError(f"Only {Color.BLACK} and {Color.WHITE} have opponents")

        return Color.BLACK if self is Color.WHITE else Color.WHITE


__all__ = ("Color",)
