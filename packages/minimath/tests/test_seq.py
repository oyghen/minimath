import itertools
from contextlib import nullcontext
from typing import TypeAlias

import minimath
import pytest

ContextManager: TypeAlias = (
    nullcontext[None] | pytest.RaisesExc[ValueError] | pytest.RaisesExc[TypeError]
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
        gen = minimath.seq.collatz(n)
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
    gen = minimath.seq.fibonacci(a, b)
    result = tuple(itertools.islice(gen, len(expected)))
    assert result == expected
