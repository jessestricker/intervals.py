import pytest

from intervals import Interval


def test_init_empty() -> None:
    empty = Interval()
    assert empty.start == 1
    assert empty.end == 0


def test_init_degenerate() -> None:
    degenerate = Interval(1)
    assert degenerate.start == 1
    assert degenerate.end == 1


def test_init_proper() -> None:
    degenerate = Interval(1, 3)
    assert degenerate.start == 1
    assert degenerate.end == 3


def test_init_proper_invalid() -> None:
    # degenerate
    with pytest.raises(ValueError):
        Interval(1, 1)

    # empty
    with pytest.raises(ValueError):
        Interval(2, 0)


def test_is_empty() -> None:
    assert Interval().is_empty

    assert not Interval(0).is_empty
    assert not Interval(1).is_empty

    assert not Interval(0, 1).is_empty
    assert not Interval(1, 3).is_empty


def test_is_degenerate() -> None:
    assert not Interval().is_degenerate

    assert Interval(0).is_degenerate
    assert Interval(1).is_degenerate

    assert not Interval(0, 1).is_degenerate
    assert not Interval(1, 3).is_degenerate


def test_is_proper() -> None:
    assert not Interval().is_proper

    assert not Interval(0).is_proper
    assert not Interval(1).is_proper

    assert Interval(0, 1).is_proper
    assert Interval(1, 3).is_proper


def test_repr() -> None:
    assert repr(Interval()) == "Interval()"

    assert repr(Interval(0)) == "Interval(0)"
    assert repr(Interval(1)) == "Interval(1)"
    assert repr(Interval(2)) == "Interval(2)"

    assert repr(Interval(0, 1)) == "Interval(0, 1)"
    assert repr(Interval(0, 2)) == "Interval(0, 2)"
    assert repr(Interval(1, 2)) == "Interval(1, 2)"


def test_str() -> None:
    assert str(Interval()) == "[]"

    assert str(Interval(0)) == "[0]"
    assert str(Interval(1)) == "[1]"
    assert str(Interval(2)) == "[2]"

    assert str(Interval(0, 1)) == "[0..1]"
    assert str(Interval(0, 2)) == "[0..2]"
    assert str(Interval(1, 2)) == "[1..2]"


def test_eq_hash() -> None:
    def assert_eq_hash_sym(lhs: Interval, rhs: Interval, expected: bool) -> None:
        assert (lhs == rhs) == expected
        assert (rhs == lhs) == expected
        assert (hash(lhs) == hash(rhs)) == expected

    assert_eq_hash_sym(Interval(), Interval(), True)  # empty
    assert_eq_hash_sym(Interval(0), Interval(0), True)  # degenerate
    assert_eq_hash_sym(Interval(0, 1), Interval(0, 1), True)  # proper

    assert_eq_hash_sym(Interval(), Interval(0), False)  # empty, degenerate
    assert_eq_hash_sym(Interval(), Interval(0, 1), False)  # empty, proper
    assert_eq_hash_sym(Interval(0), Interval(1), False)  # degenerate, degenerate
    assert_eq_hash_sym(Interval(0), Interval(0, 1), False)  # degenerate, proper
    assert_eq_hash_sym(Interval(0, 1), Interval(0, 2), False)  # proper, proper


def test_len() -> None:
    assert len(Interval()) == 0

    assert len(Interval(0)) == 1
    assert len(Interval(1)) == 1

    assert len(Interval(0, 1)) == 2
    assert len(Interval(1, 3)) == 3


def test_iter() -> None:
    # pylint: disable-next=use-implicit-booleaness-not-comparison
    assert list(iter(Interval())) == []

    assert list(iter(Interval(1))) == [1]
    assert list(iter(Interval(1, 3))) == [1, 2, 3]


def test_contains() -> None:
    assert -1 not in Interval()
    assert 0 not in Interval()
    assert 1 not in Interval()
    assert 2 not in Interval()

    assert 0 not in Interval(1)
    assert 1 in Interval(1)
    assert 2 not in Interval(1)

    assert 0 not in Interval(1, 3)
    assert 1 in Interval(1, 3)
    assert 2 in Interval(1, 3)
    assert 3 in Interval(1, 3)
    assert 4 not in Interval(1, 3)


def test_subset_superset() -> None:
    def assert_is_subset_of(sub: Interval, super_: Interval, expected: bool) -> None:
        assert sub.is_subset_of(super_) == expected
        assert super_.is_superset_of(sub) == expected

    # empty, empty
    assert_is_subset_of(Interval(), (Interval()), True)
    # empty, degenerate
    assert_is_subset_of(Interval(), (Interval(1)), True)
    # empty, proper
    assert_is_subset_of(Interval(), (Interval(1, 3)), True)

    # degenerate, empty
    assert_is_subset_of(Interval(1), (Interval()), False)
    # degenerate, degenerate
    assert_is_subset_of(Interval(1), (Interval(1)), True)
    assert_is_subset_of(Interval(0), (Interval(1)), False)
    # degenerate, proper
    assert_is_subset_of(Interval(0), (Interval(1, 3)), False)
    assert_is_subset_of(Interval(1), (Interval(1, 3)), True)
    assert_is_subset_of(Interval(2), (Interval(1, 3)), True)
    assert_is_subset_of(Interval(3), (Interval(1, 3)), True)
    assert_is_subset_of(Interval(4), (Interval(1, 3)), False)

    # proper, empty
    assert_is_subset_of(Interval(1, 3), (Interval()), False)
    # proper, degenerate
    assert_is_subset_of(Interval(1, 3), (Interval(0)), False)
    assert_is_subset_of(Interval(1, 3), (Interval(1)), False)
    assert_is_subset_of(Interval(1, 3), (Interval(2)), False)
    assert_is_subset_of(Interval(1, 3), (Interval(3)), False)
    assert_is_subset_of(Interval(1, 3), (Interval(4)), False)
    # proper, proper
    assert_is_subset_of(Interval(1, 3), (Interval(1, 2)), False)
    assert_is_subset_of(Interval(1, 3), (Interval(1, 3)), True)
    assert_is_subset_of(Interval(1, 3), (Interval(1, 4)), True)


def test_intersection_and_disjoint() -> None:
    def assert_intersection_sym(
        lhs: Interval, rhs: Interval, expected: Interval
    ) -> None:
        assert lhs.intersection(rhs) == expected
        assert rhs.intersection(lhs) == expected
        assert lhs.is_disjoint_from(rhs) == expected.is_empty
        assert rhs.is_disjoint_from(lhs) == expected.is_empty

    # empty, empty
    assert_intersection_sym(Interval(), Interval(), Interval())

    # empty, degenerate
    assert_intersection_sym(Interval(), Interval(1), Interval())

    # empty, proper
    assert_intersection_sym(Interval(), Interval(1, 3), Interval())

    # degenerate, degenerate
    assert_intersection_sym(Interval(1), Interval(1), Interval(1))
    assert_intersection_sym(Interval(1), Interval(2), Interval())

    # degenerate, proper
    assert_intersection_sym(Interval(0), Interval(1, 3), Interval())
    assert_intersection_sym(Interval(1), Interval(1, 3), Interval(1))
    assert_intersection_sym(Interval(2), Interval(1, 3), Interval(2))
    assert_intersection_sym(Interval(3), Interval(1, 3), Interval(3))
    assert_intersection_sym(Interval(4), Interval(1, 3), Interval())

    # proper, proper
    assert_intersection_sym(Interval(0, 1), Interval(2, 4), Interval())
    assert_intersection_sym(Interval(0, 2), Interval(2, 4), Interval(2))
    assert_intersection_sym(Interval(0, 3), Interval(2, 4), Interval(2, 3))
    assert_intersection_sym(Interval(0, 4), Interval(2, 4), Interval(2, 4))
    assert_intersection_sym(Interval(0, 5), Interval(2, 4), Interval(2, 4))

    assert_intersection_sym(Interval(1, 2), Interval(2, 4), Interval(2))
    assert_intersection_sym(Interval(1, 3), Interval(2, 4), Interval(2, 3))
    assert_intersection_sym(Interval(1, 4), Interval(2, 4), Interval(2, 4))
    assert_intersection_sym(Interval(1, 5), Interval(2, 4), Interval(2, 4))

    assert_intersection_sym(Interval(2, 3), Interval(2, 4), Interval(2, 3))
    assert_intersection_sym(Interval(2, 4), Interval(2, 4), Interval(2, 4))
    assert_intersection_sym(Interval(2, 5), Interval(2, 4), Interval(2, 4))

    assert_intersection_sym(Interval(3, 4), Interval(2, 4), Interval(3, 4))
    assert_intersection_sym(Interval(3, 5), Interval(2, 4), Interval(3, 4))

    assert_intersection_sym(Interval(4, 5), Interval(2, 4), Interval(4))
    assert_intersection_sym(Interval(5, 6), Interval(2, 4), Interval())
