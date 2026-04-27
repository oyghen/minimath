import sys
from collections.abc import Iterable, Set

import minimath
import pytest


class TestTwoSetSummary:
    def test_summarize_str_sets(self):
        set1 = {"a", "c", "b", "g", "h"}
        set2 = {"c", "d", "e", "f", "g"}
        summary = minimath.sets.summarize(set1, set2)

        assert isinstance(summary, minimath.sets.TwoSetSummary)
        assert isinstance(summary.set1, frozenset)
        assert isinstance(summary.set2, frozenset)
        assert summary.set1 == frozenset(set1)
        assert summary.set2 == frozenset(set2)

        assert summary.union == frozenset({"a", "c", "b", "g", "h", "d", "e", "f"})
        assert summary.intersection == frozenset({"c", "g"})
        assert summary.set1_minus_set2 == frozenset({"a", "b", "h"})
        assert summary.set2_minus_set1 == frozenset({"d", "e", "f"})
        assert summary.sym_diff == frozenset({"a", "b", "h", "d", "e", "f"})

        assert summary.jaccard_score == 0.25
        assert summary.overlap_score == 0.4
        assert summary.dice_score == 0.4

        assert summary.is_equal is False
        assert summary.is_disjoint is False
        assert summary.is_subset is False
        assert summary.is_strict_subset is False

    def test_summarize_int_sets(self):
        set1 = {1, 2, 3}
        set2 = {2, 3, 4, 5}
        summary = minimath.sets.summarize(set1, set2)

        assert isinstance(summary, minimath.sets.TwoSetSummary)
        assert isinstance(summary.set1, frozenset)
        assert isinstance(summary.set2, frozenset)
        assert summary.set1 == frozenset(set1)
        assert summary.set2 == frozenset(set2)

        assert summary.union == frozenset({1, 2, 3, 4, 5})
        assert summary.intersection == frozenset({2, 3})
        assert summary.set1_minus_set2 == frozenset({1})
        assert summary.set2_minus_set1 == frozenset({4, 5})
        assert summary.sym_diff == frozenset({1, 4, 5})

        assert summary.jaccard_score == pytest.approx(minimath.sets.jaccard(set1, set2))
        assert summary.overlap_score == pytest.approx(minimath.sets.overlap(set1, set2))
        assert summary.dice_score == pytest.approx(minimath.sets.dice(set1, set2))

        assert summary.is_equal is False
        assert summary.is_disjoint is False
        assert summary.is_subset is False
        assert summary.is_strict_subset is False

    @pytest.mark.parametrize(
        "set1, set2, expected_jaccard, expected_overlap, expected_dice",
        [
            (set(), set(), 1.0, 1.0, 1.0),
            ({"a"}, {"a"}, 1.0, 1.0, 1.0),
            ({"a"}, {"b"}, 0.0, 0.0, 0.0),
            ({"a", "b"}, {"b", "c"}, 1 / 3, 1 / 2, 2 / 4),
        ],
        ids=[
            "empty vs empty",
            "identical singletons",
            "disjoint singletons",
            "overlapping sets",
        ],
    )
    def test_metric_values(
        self,
        set1: set[str],
        set2: set[str],
        expected_jaccard: float,
        expected_overlap: float,
        expected_dice: float,
    ):
        # symmetric checks
        assert minimath.sets.jaccard(set1, set2) == pytest.approx(expected_jaccard)
        assert minimath.sets.jaccard(set2, set1) == pytest.approx(expected_jaccard)

        assert minimath.sets.overlap(set1, set2) == pytest.approx(expected_overlap)
        assert minimath.sets.overlap(set2, set1) == pytest.approx(expected_overlap)

        assert minimath.sets.dice(set1, set2) == pytest.approx(expected_dice)
        assert minimath.sets.dice(set2, set1) == pytest.approx(expected_dice)

    def test_iterable_inputs(self):
        some_list = ["x", "y"]
        some_tuple = ("y", "z")
        some_generator = (c for c in ["y", "z"])

        summary1 = minimath.sets.summarize(some_list, some_tuple)
        summary2 = minimath.sets.summarize(some_list, some_generator)

        assert summary1.intersection == frozenset({"y"})
        assert summary2.intersection == frozenset({"y"})

        assert minimath.sets.jaccard(some_list, some_tuple) == pytest.approx(1 / 3)
        assert minimath.sets.overlap(some_list, some_tuple) == pytest.approx(1 / 2)
        assert minimath.sets.dice(some_list, some_tuple) == pytest.approx(2 / 4)

    def test_strict_subset_and_subset_flags(self):
        set1 = {1, 2}
        set2 = {1, 2, 3}
        summary = minimath.sets.summarize(set1, set2)
        assert summary.is_subset is True
        assert summary.is_strict_subset is True
        assert summary.is_equal is False

        summary_rev = minimath.sets.summarize(set2, set1)
        assert summary_rev.is_subset is False
        assert summary_rev.is_strict_subset is False

    def test_equal_flag(self):
        set1 = {1, 2}
        set2 = {1, 2}
        summary = minimath.sets.summarize(set1, set2)
        assert summary.is_equal is True
        assert summary.is_subset is True
        assert summary.is_strict_subset is False

        summary_rev = minimath.sets.summarize(set2, set1)
        assert summary_rev.is_equal is True
        assert summary_rev.is_subset is True
        assert summary_rev.is_strict_subset is False

    def test_floating_point_edge_cases(self):
        set1 = set(range(1000))
        set2 = set(range(500, 1500))
        jaccard_score = minimath.sets.jaccard(set1, set2)
        overlap_score = minimath.sets.overlap(set1, set2)
        dice_score = minimath.sets.dice(set1, set2)

        assert 0.0 <= jaccard_score <= 1.0
        assert 0.0 <= overlap_score <= 1.0
        assert 0.0 <= dice_score <= 1.0

        eps = sys.float_info.epsilon
        assert dice_score >= jaccard_score - eps

    def test_type_and_immutability(self):
        summary = minimath.sets.summarize([1, 2], [2, 3])
        with pytest.raises((AttributeError, TypeError)):
            summary.set1 = frozenset()  # type: ignore


class TestUnion:
    @pytest.mark.parametrize(
        "sets, expected",
        [
            ([{1, 2, 3}], {1, 2, 3}),
            ([{1, 2}, {3, 4}], {1, 2, 3, 4}),
            ([{1, 2}, {3}, {2, 4}], {1, 2, 3, 4}),
            ([{1, 2}, {2, 3}, {3, 4}], {1, 2, 3, 4}),
            ([set(), {1}, set(), {2, 3}], {1, 2, 3}),
        ],
    )
    def test_basic_cases(self, sets: Iterable[Set[int]], expected: set[int]):
        assert minimath.sets.union(sets) == expected  # type: ignore

    def test_empty_input(self):
        assert minimath.sets.union([]) == set()

    def test_single_set(self):
        s = {42}
        assert minimath.sets.union([s]) == {42}

    def test_overlap(self):
        assert minimath.sets.union([{1, 2}, {2, 3}, {3, 1}]) == {1, 2, 3}

    def test_no_mutation_of_inputs(self):
        a = {1, 2}
        b = {3}
        orig_a = a.copy()
        orig_b = b.copy()

        u = minimath.sets.union([a, b])

        assert a == orig_a
        assert b == orig_b
        assert u == {1, 2, 3}

    def test_type_preservation(self):
        s1: set[str] = {"a", "b"}
        s2: set[str] = {"b", "c"}
        result = minimath.sets.union([s1, s2])
        assert result == {"a", "b", "c"}
        assert all(isinstance(x, str) for x in result)

    def test_iterable_input(self):
        iterable = [{1}, {2, 3}, {3, 4}]
        result = minimath.sets.union(iterable)
        assert result == {1, 2, 3, 4}

    def test_accepts_iterators(self):
        sets = ({i, i + 1} for i in range(3))
        assert minimath.sets.union(sets) == {0, 1, 2, 3}

    def test_heterogeneous_iterable_inputs(self):
        sets = [
            {1, 2},
            (i for i in (2, 3)),
            {i for i in range(3, 5)},
        ]
        result = minimath.sets.union(sets)  # type: ignore
        assert result == {1, 2, 3, 4}

    @pytest.mark.parametrize(
        "sets",
        [
            [{1, 2}, {3.0, 4.0}],
            [{"a", "b"}, {"c"}],
            [{(1, 2)}, {(3, 4)}],
        ],
    )
    def test_heterogeneous_hashable_elements(self, sets: Iterable[Set[int | str]]):
        result = minimath.sets.union(sets)  # type: ignore
        assert len(result) == sum(len(s) for s in sets)
        for s in sets:
            assert s.issubset(result)  # type: ignore

    def test_large_input(self):
        sets = [set(range(i, i + 100)) for i in range(0, 1000, 100)]
        result = minimath.sets.union(sets)
        assert result == set(range(0, 1000))


class TestIntersect:
    def test_basic(self):
        a = {1, 2, 3}
        b = {2, 3}
        c = {3}

        result = minimath.sets.intersect([a, b, c])

        assert result == {3}

    def test_empty_input(self):
        result = minimath.sets.intersect([])
        assert result == set()

    def test_single_set(self):
        s = {42}
        result = minimath.sets.intersect([s])
        assert result == {42}

    def test_disjoint_sets(self):
        a = {1, 2}
        b = {3, 4}

        result = minimath.sets.intersect([a, b])

        assert result == set()

    def test_overlap(self):
        a = {1, 2, 3}
        b = {2, 3, 4}

        result = minimath.sets.intersect([a, b])

        assert result == {2, 3}

    def test_intersect_with_empty_set(self):
        a = {1, 2, 3}
        b = {}
        c = {2, 3, 4}

        result = minimath.sets.intersect([a, b, c])  # type: ignore

        assert result == set()

    def test_heterogeneous_iterable_inputs(self):
        sets = [
            {1, 2},
            (i for i in (2, 3)),
            {i for i in range(2, 5)},
        ]
        result = minimath.sets.intersect(sets)  # type: ignore
        assert result == {2}

    def test_no_mutation(self):
        a = {1, 2, 3}
        b = {2, 3, 4}
        orig_a = a.copy()
        orig_b = b.copy()

        result = minimath.sets.intersect([a, b])

        assert a == orig_a
        assert b == orig_b
        assert result == {2, 3}

    def test_type_preservation(self):
        s1: set[str] = {"a", "b", "c"}
        s2: set[str] = {"b", "c", "d"}

        result = minimath.sets.intersect([s1, s2])

        assert result == {"b", "c"}
        assert all(isinstance(x, str) for x in result)
