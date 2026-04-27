import math
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


@pytest.mark.parametrize(
    "number, expected",
    [
        (-2.0, -1.0),
        (-1, -1.0),
        (-0, 0.0),
        (0, 0.0),
        (1, 1.0),
        (2.0, 1.0),
        (float("inf"), 1.0),
        (float("-inf"), -1.0),
        (math.nan, math.nan),
    ],
)
def test_sign(number: int | float, expected: float):
    result = minimath.core.sign(number)
    assert isinstance(result, float)
    if math.isnan(expected):
        assert math.isnan(result)
    else:
        assert result == expected


@pytest.mark.parametrize(
    "number, num_digits, expected, ctx",
    [
        # valid cases
        (987654321.123456789, 1, 1000000000.0, nullcontext()),
        (987654321.123456789, 2, 990000000.0, nullcontext()),
        (987654321.123456789, 3, 988000000.0, nullcontext()),
        (987654321.123456789, 4, 987700000.0, nullcontext()),
        (987654321.123456789, 5, 987650000.0, nullcontext()),
        (987654321.123456789, 6, 987654000.0, nullcontext()),
        (987654321.123456789, 7, 987654300.0, nullcontext()),
        (987654321.123456789, 8, 987654320.0, nullcontext()),
        (987654321.123456789, 9, 987654321.0, nullcontext()),
        (987654321.123456789, 10, 987654321.1, nullcontext()),
        (987654321.123456789, 11, 987654321.12, nullcontext()),
        (987654321.123456789, 12, 987654321.123, nullcontext()),
        (987654321.123456789, 13, 987654321.1235, nullcontext()),
        (1.123456789, 1, 1.0, nullcontext()),
        (1.123456789, 2, 1.1, nullcontext()),
        (1.123456789, 3, 1.12, nullcontext()),
        (1.123456789, 4, 1.123, nullcontext()),
        (0.123456789, 1, 0.1, nullcontext()),
        (0.123456789, 2, 0.12, nullcontext()),
        (0.123456789, 3, 0.123, nullcontext()),
        (0.123456789, 4, 0.1235, nullcontext()),
        (-1.4142135623730951, 1, -1.0, nullcontext()),
        (-1.4142135623730951, 2, -1.4, nullcontext()),
        (-1.4142135623730951, 3, -1.41, nullcontext()),
        (-1.4142135623730951, 4, -1.414, nullcontext()),
        (14393237.76, 1, 10000000.0, nullcontext()),
        (14393237.76, 2, 14000000.0, nullcontext()),
        (14393237.76, 3, 14400000.0, nullcontext()),
        (14393237.76, 4, 14390000.0, nullcontext()),
        (1234, 1, 1000, nullcontext()),
        (1234, 2, 1200, nullcontext()),
        (1234, 3, 1230, nullcontext()),
        (1234, 4, 1234, nullcontext()),
        (1234, 5, 1234, nullcontext()),
        (1234, 9, 1234, nullcontext()),
        (5678, 1, 6000, nullcontext()),
        (5678, 2, 5700, nullcontext()),
        (5678, 3, 5680, nullcontext()),
        (5678, 4, 5678, nullcontext()),
        (5123, 1, 5000, nullcontext()),
        (5123, 2, 5100, nullcontext()),
        (5123, 3, 5120, nullcontext()),
        (5123, 4, 5123, nullcontext()),
        (1, 3, 1, nullcontext()),
        (10, 3, 10, nullcontext()),
        (100, 3, 100, nullcontext()),
        (1000, 3, 1000, nullcontext()),
        # edge cases
        (math.inf, 3, math.inf, nullcontext()),
        (0, 3, 0, nullcontext()),
        (0.0, 3, 0.0, nullcontext()),
        (1e-12, 3, 1e-12, nullcontext()),
        # invalid cases
        (1, -1, None, pytest.raises(ValueError)),
        (2, 0, None, pytest.raises(ValueError)),
        (3, 0.0, None, pytest.raises(TypeError)),
        (4, 1.0, None, pytest.raises(TypeError)),
    ],
)
def test_signif(
    number: int | float,
    num_digits: int,
    expected: int | float,
    ctx: ContextManager,
):
    with ctx:
        result = minimath.core.signif(number, num_digits)
        assert result == expected
