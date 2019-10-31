# Internal
import typing as T
from abc import abstractmethod

# External
import typing_extensions as Te


class ViewProtocol(Te.Protocol):
    automatic: bool
    player_paths: T.Sequence[str]

    @abstractmethod
    def loop(self) -> None:
        ...

    @abstractmethod
    def input(self, msg: str) -> str:
        ...

    @abstractmethod
    def alert(self, msg: str) -> None:
        ...
