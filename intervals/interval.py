from collections.abc import Collection, Hashable, Iterator
from types import NotImplementedType
from typing import Self, overload


class Interval(Collection[int], Hashable):
    """A closed and bounded integer interval [start..end].

    An interval may be classified as either one of these types:
    - *empty*, contains zero elements: if start > end
    - *degenerate*, contains exactly one element: if start = end
    - *proper*, contains more than one elements: if start < end
    """

    @overload
    def __init__(self) -> None:
        """Create an empty interval."""

    @overload
    def __init__(self, element: int, /) -> None:
        """Create a degenerate interval with a single element."""

    @overload
    def __init__(self, start: int, end: int, /) -> None:
        """Create a proper interval from two endpoints where `start` < `end`."""

    def __init__(self, *args: int) -> None:
        match len(args):
            case 0:  # empty overload
                start = 1
                end = 0
            case 1:  # degenerate overload
                start = args[0]
                end = args[0]
            case 2:  # proper overload
                start = args[0]
                end = args[1]
                if not start < end:
                    raise ValueError("proper interval requires start < end")
            case _:  # no overload, error
                raise ValueError(
                    "this function takes either none, one or two arguments"
                )
        self._start = start
        self._end = end

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end

    @property
    def is_empty(self) -> bool:
        return self.start > self.end

    @property
    def is_degenerate(self) -> bool:
        return self.start == self.end

    @property
    def is_proper(self) -> bool:
        return self.start < self.end

    def __repr__(self) -> str:
        if self.is_empty:
            return "Interval()"
        if self.is_degenerate:
            return f"Interval({self.start!r})"
        return f"Interval({self.start!r}, {self.end!r})"

    def __str__(self) -> str:
        if self.is_empty:
            return "[]"
        if self.is_degenerate:
            return f"[{self.start!r}]"
        return f"[{self.start!r}..{self.end!r}]"

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Interval):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __len__(self) -> int:
        if self.is_empty:
            return 0
        return self.end - self.start + 1

    def __iter__(self) -> Iterator[int]:
        if self.is_empty:
            return iter(())
        return iter(range(self.start, self.end + 1))

    def __contains__(self, item: object) -> bool | NotImplementedType:
        if not isinstance(item, int):
            return NotImplemented
        return self.start <= item <= self.end

    def is_subset_of(self, other: Self) -> bool:
        return self.is_empty or ((self.start in other) and (self.end in other))

    def is_superset_of(self, other: Self) -> bool:
        return other.is_subset_of(self)
