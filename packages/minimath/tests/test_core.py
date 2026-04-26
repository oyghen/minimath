import pytest
from minimath.core import is_even, is_odd


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
    assert is_even(number) == expected


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
    assert is_odd(number) == expected
