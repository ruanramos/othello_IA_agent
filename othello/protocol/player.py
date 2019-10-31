# Internal
import typing as T

# External
import typing_extensions as Te

if T.TYPE_CHECKING:
    # Project
    from ..enums import Color
    from ..models import Board, Position


@Te.runtime
class PlayerProtocol(Te.Protocol):
    def play(self, __board: "Board", **__kwargs: T.Any) -> "Position":
        ...


class ColoredPlayerProtocol(PlayerProtocol):
    color: "Color"

    def __init__(self, __color: "Color"):
        self.color = __color
