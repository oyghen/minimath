from contextlib import nullcontext
from typing import TypeAlias

import minimath
import pytest

ContextManager: TypeAlias = nullcontext[None] | pytest.RaisesExc[ZeroDivisionError]


@pytest.mark.parametrize(
    "number, by, expected, ctx",
    [
        (-1, 2, False, nullcontext()),
        (0, 2, True, nullcontext()),
        (1, 2, False, nullcontext()),
        (2, 2, True, nullcontext()),
        (3, 2, False, nullcontext()),
        (4, 2, True, nullcontext()),
        (5, 2, False, nullcontext()),
        (6, 2, True, nullcontext()),
        (7, 2, False, nullcontext()),
        (8, 2, True, nullcontext()),
        (9, 2, False, nullcontext()),
        (10, 2, True, nullcontext()),
        (10, 5, True, nullcontext()),
        (11, 2, False, nullcontext()),
        (10, 0, True, pytest.raises(ZeroDivisionError)),
    ],
)
def test_is_divisible(number: int, by: int, expected: bool, ctx: ContextManager):
    with ctx:
        result = minimath.core.is_divisible(number, by)
        assert result == expected


@pytest.mark.parametrize(
    "number, expected",
    [
        (-1, False),
        (0, True),
        (1, False),
        (2, True),
        (3, False),
        (4, True),
        (5, False),
        (6, True),
        (7, False),
        (8, True),
        (9, False),
        (10, True),
        (10.0, True),
        (11.0, False),
    ],
)
def test_is_even(number: int | float, expected: bool):
    assert minimath.core.is_even(number) == expected


@pytest.mark.parametrize(
    "number, expected",
    [
        (-1, True),
        (0, False),
        (1, True),
        (2, False),
        (3, True),
        (4, False),
        (5, True),
        (6, False),
        (7, True),
        (8, False),
        (9, True),
        (10, False),
        (10.0, False),
        (11.0, True),
    ],
)
def test_is_odd(number: int | float, expected: bool):
    assert minimath.core.is_odd(number) == expected


class TestPad:
    @pytest.mark.parametrize(
        "lower, upper, fraction, expected",
        [
            (0.0, 1.0, 0.05, (-0.05, 1.05)),
            (0.0, 1.0, 0.1, (-0.1, 1.1)),
            (1.0, 0.0, 0.05, (-0.05, 1.05)),
            (0, 10, 0.1, (-1.0, 11.0)),
            (0.0, 1.0, -0.2, (0.2, 0.8)),
            (0.0, 1.0, 2.0, (-2.0, 3.0)),
        ],
        ids=[
            "fraction=0.05",
            "fraction=0.10",
            "inverted inputs",
            "int inputs coerced to float",
            "negative fraction (shrinks interval)",
            "large fraction",
        ],
    )
    def test_various_cases(
        self,
        lower: float,
        upper: float,
        fraction: float,
        expected: tuple[float, float],
    ):
        result = minimath.core.pad(lower, upper, fraction)
        assert isinstance(result, tuple)
        assert all(isinstance(x, float) for x in result)
        assert result == pytest.approx(expected)

    def test_zero_length_interval(self):
        assert minimath.core.pad(2.0, 2.0) == (2.0, 2.0)

    def test_symmetry_with_inverted_inputs(self):
        assert minimath.core.pad(0.0, 1.0) == minimath.core.pad(1.0, 0.0)

    def test_default_fraction(self):
        assert minimath.core.pad(0.0, 1.0) == pytest.approx((-0.05, 1.05))
