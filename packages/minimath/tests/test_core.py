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


class TestDlog:
    @pytest.mark.parametrize(
        "number, expected",
        [
            (0, 0.0),
            (0.1, 0.0),
            (1, 1.0),
            (10, 2.0),
            (100, 3.0),
            (1_000, 4.0),
            (10_000, 5.0),
            (100_000, 6.0),
            (1_000_000, 7.0),
            (0.2, 0.30102999566398125),
            (2, 1.3010299956639813),
            (20, 2.3010299956639813),
            (200, 3.3010299956639813),
            (2_000, 4.3010299956639813),
            (-0.5, 0.6989700043360187),
            (-5, 1.6989700043360187),
            (-50, 2.6989700043360187),
            (-500, 3.6989700043360187),
            (-5_000, 4.6989700043360187),
        ],
    )
    def test_log(self, number: int | float, expected: float):
        for v in (-number, number):
            result = core.dlog(v)
            assert isinstance(result, float)
            assert result == expected

    @pytest.mark.parametrize(
        "number, expected",
        [
            (0, 0),
            (0.1, 0),
            (1, 1),
            (10, 2),
            (100, 3),
            (1_000, 4),
            (10_000, 5),
            (100_000, 6),
            (1_000_000, 7),
            (0.2, 0),
            (2, 1),
            (20, 2),
            (200, 3),
            (2_000, 4),
            (-0.5, 0),
            (-5, 1),
            (-50, 2),
            (-500, 3),
            (-5_000, 4),
        ],
    )
    def test_int(self, number: int | float, expected: int):
        for v in (-number, number):
            result = core.dlog(v, kind="int")
            assert isinstance(result, int)
            assert result == expected

    @pytest.mark.parametrize(
        "number, expected",
        [
            (0, 0.0),
            (0.1, 0.0),
            (1, 1.0),
            (10, 2.0),
            (100, 3.0),
            (1_000, 4.0),
            (10_000, 5.0),
            (100_000, 6.0),
            (1_000_000, 7.0),
            (0.2, 0.11111111111111112),
            (2, 1.1111111111111112),
            (20, 2.111111111111111),
            (200, 3.111111111111111),
            (2_000, 4.111111111111111),
            (-0.5, 0.4444444444444445),
            (-5, 1.4444444444444444),
            (-50, 2.4444444444444446),
            (-500, 3.4444444444444446),
            (-5_000, 4.444444444444445),
        ],
    )
    def test_linear(self, number: int | float, expected: int):
        for v in (-number, number):
            result = core.dlog(v, kind="linear")
            assert isinstance(result, float)
            assert result == expected

    @pytest.mark.parametrize(
        "number, expected",
        [
            (0, 0),
            (1, 1),
            (10, 2),
            (100, 3),
            (1_000, 4),
            (0.1, 0),
            (1.1, 1.0413926851582251),
            (10.1, 2.0043213737826426),
            (100.1, 3.000434077479319),
            (1_000.1, 4.000043427276863),
        ],
    )
    def test_decimal_numbers(self, number: int | float, expected: int | float):
        for v in (-number, number):
            result = core.dlog(v)
            assert isinstance(result, float)
            assert result == expected

    @pytest.mark.parametrize("kind", [None, "LOG", 1, 2.0, "invalid_kind"])
    def test_invalid_values(self, kind: str):
        with pytest.raises(ValueError):
            core.dlog(10, kind=kind)


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
