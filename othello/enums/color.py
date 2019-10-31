# Internal
from enum import Enum, unique


@unique
class Color(Enum):
    EMPTY = "."
    BLACK = "@"
    WHITE = "o"
    OUTER = "?"

    def opposite(self) -> "Color":
        if self in (Color.EMPTY, Color.OUTER):
            raise ValueError(f"Only {Color.BLACK} and {Color.WHITE} have opponents")

        return Color.BLACK if self is Color.WHITE else Color.WHITE


__all__ = ("Color",)
