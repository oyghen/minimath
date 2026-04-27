__all__ = ("identity", "dlog")

import math
from typing import Literal, TypeVar, get_args

T = TypeVar("T")


def identity(value: T, /) -> T:
    """Return value unchanged."""
    return value


def dlog(
    number: int | float,
    /,
    *,
    kind: Literal["log", "int", "linear"] = "log",
) -> int | float:
    """Return scaled value whose integer part equals the original main digit count."""
    choices = get_args(dlog.__annotations__["kind"])
    if kind not in choices:
        raise ValueError(f"invalid kind {kind!r}: expected one of {choices}")

    x = abs(number)
    fx = 1 + math.log10(x) if x >= 0.1 else 0.0

    match kind:
        case "log":
            return fx

        case "int":
            return math.floor(fx)

        case "linear":
            n = math.floor(fx)
            y0, y1 = n, n + 1
            x0, x1 = 10 ** (n - 1), 10**n
            return (y0 * (x1 - x) + y1 * (x - x0)) / (x1 - x0) if x >= 0.1 else 0.0
