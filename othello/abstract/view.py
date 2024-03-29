# Internal
import typing as T
from abc import ABCMeta, abstractmethod

# Type generics
K = T.TypeVar("K", bound="AbstractView")


class AbstractView(metaclass=ABCMeta):
    automatic: bool
    player_paths: T.Sequence[str]

    class Model(T.Generic[K], metaclass=ABCMeta):
        def __init__(self, title: str):
            self._title = title
            self._structure: T.List[T.Tuple[str, T.Dict[str, T.Any]]] = []

        def add_input(self, label: str) -> None:
            self._structure.append(("input", {"label": label}))

        def add_paragraph(self, text: str) -> None:
            self._structure.append(("paragraph", {"text": text}))

        @abstractmethod
        def show(self, view: K) -> T.Sequence[T.Any]:
            ...

    @classmethod
    @abstractmethod
    def available(cls) -> bool:
        ...

    def __init__(
        self, player_paths: T.Optional[T.Sequence[str]] = None, automatic: bool = False,
    ) -> None:
        self.automatic = automatic
        self.player_paths = player_paths or tuple()

    @abstractmethod
    def loop(self) -> None:
        ...

    @abstractmethod
    def input(self, label: str) -> str:
        ...

    @abstractmethod
    def alert(self, msg: str) -> None:
        ...
