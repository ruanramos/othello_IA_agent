# Internal
import typing as T

# Type generics
K = T.TypeVar("K")


class LineView(T.MutableSequence[K]):
    def __init__(
        self, line: int, mapping: T.MutableMapping[T.Tuple[int, int], K],
    ):
        self._line = line
        self._mapping = mapping

    def __len__(self) -> int:
        return len(tuple(self))

    def __iter__(self) -> T.Iterator[K]:
        for (i, j), value in self._mapping.items():
            if j == self._line:
                yield value

    @T.overload
    def __getitem__(self, column: int) -> K:
        ...

    @T.overload
    def __getitem__(self, column: slice) -> T.List[K]:
        ...

    def __getitem__(self, column: T.Union[int, slice]) -> T.Union[K, T.List[K]]:
        if isinstance(column, slice):
            return [self._mapping[i, self._line] for i in range(column.start, column.stop)]

        return self._mapping[column, self._line]

    @T.overload
    def __setitem__(self, column: int, value: K) -> None:
        ...

    @T.overload
    def __setitem__(self, column: slice, value: T.Iterable[K]) -> None:
        ...

    def __setitem__(self, column: T.Union[int, slice], value: T.Union[K, T.Iterable[K]]) -> None:
        if isinstance(column, slice):
            for i, v in enumerate(value):
                self._mapping[column.start + i, self._line] = v

            return

        self._mapping[column, self._line] = value

    def __delitem__(self, column: T.Union[int, slice]) -> None:
        raise IndexError

    def insert(self, _: int, __: K) -> None:
        raise IndexError
