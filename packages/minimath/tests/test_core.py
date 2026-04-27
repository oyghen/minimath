import itertools
from contextlib import nullcontext
from typing import TypeAlias

import pytest
from minimath import core

ContextManager: TypeAlias = (
    nullcontext[None]
    | pytest.RaisesExc[ValueError]
    | pytest.RaisesExc[TypeError]
    | pytest.RaisesExc[ZeroDivisionError]
)


@pytest.mark.parametrize(
    "n, expected, ctx",
    [
        (1, (1,), nullcontext()),
        (2, (2, 1), nullcontext()),
        (4, (4, 2, 1), nullcontext()),
        (
            7,
            (7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1),
            nullcontext(),
        ),
        (11, (11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1), nullcontext()),
        (12, (12, 6, 3, 10, 5, 16, 8, 4, 2, 1), nullcontext()),
        (-2, None, pytest.raises(ValueError)),
        (-1, None, pytest.raises(ValueError)),
        (0, None, pytest.raises(ValueError)),
        (0.5, None, pytest.raises(TypeError)),
    ],
)
def test_collatz(n: int, expected: tuple[int], ctx: ContextManager):
    with ctx:
        gen = core.collatz(n)
        assert tuple(gen) == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (0, 1, ()),
        (0, 1, (0,)),
        (0, 1, (0, 1)),
        (0, 1, (0, 1, 1)),
        (0, 1, (0, 1, 1, 2)),
        (0, 1, (0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987)),
        (1, 1, (1, 1, 2, 3)),
        (13, 21, ()),
        (13, 21, (13,)),
        (13, 21, (13, 21)),
        (13, 21, (13, 21, 34, 55, 89, 144)),
        (6, 7, (6, 7, 13, 20, 33, 53, 86, 139)),
    ],
)
def test_fibonacci(a: int, b: int, expected: tuple[int]):
    gen = core.fibonacci(a, b)
    result = tuple(itertools.islice(gen, len(expected)))
    assert result == expected


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
        result = core.is_divisible(number, by)
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
    assert core.is_even(number) == expected


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
    assert core.is_odd(number) == expected
