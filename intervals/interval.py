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
            case 0:
                # empty interval
                self._start = 1
                self._end = 0
            case 1:
                # degenerate interval
                self._start = args[0]
                self._end = args[0]
            case 2:
                # proper interval
                self._start = args[0]
                self._end = args[1]
                if not self._start < self._end:  # pylint: disable=unneeded-not
                    raise ValueError("proper interval requires start < end")
            case _:
                # invalid overload
                raise ValueError(
                    "this function takes either none, one or two arguments"
                )

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
        if self.is_empty:
            return True
        return (self.start in other) and (self.end in other)

    def is_superset_of(self, other: Self) -> bool:
        return other.is_subset_of(self)

    def is_disjoint_from(self, other: Self) -> bool:
        if self.is_empty or other.is_empty:
            return True
        one_contains_endpoint_of_other = (
            other.start in self
            or other.end in self
            or self.start in other
            or self.end in other
        )
        return not one_contains_endpoint_of_other

    def intersection(self, other: Self) -> Self:
        if self.is_disjoint_from(other):
            return type(self)()
        intersection_start = max(self.start, other.start)
        intersection_end = min(self.end, other.end)
        if intersection_start == intersection_end:
            return type(self)(intersection_start)
        return type(self)(intersection_start, intersection_end)

    def is_adjacent_to(self, other: Self) -> bool:
        if self.is_empty or other.is_empty:
            return False
        return (other.end + 1) == self.start or (self.end + 1) == other.start

    def union(self, other: Self) -> Self | None:
        if self.is_empty:
            return other
        if other.is_empty:
            return self
        if not self.is_adjacent_to(other) and self.is_disjoint_from(other):
            return None
        union_start = min(self.start, other.start)
        union_end = max(self.end, other.end)
        if union_start == union_end:
            return type(self)(union_start)
        return type(self)(union_start, union_end)
