__all__ = ("dlog", "is_divisible", "is_even", "is_odd")

import math


def dlog(number: int | float, /, kind: str = "log") -> int | float:
    """Return scaled value whose integer part equals the original main digit count."""
    choices = ("log", "int", "linear")
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


def is_divisible(number: int, by: int) -> bool:
    """Return True if number is evenly divisible by the specified integer."""
    return number % by == 0


def is_even(number: int | float, /) -> bool:
    """Return True if number is even."""
    return number % 2 == 0


def is_odd(number: int | float, /) -> bool:
    """Return True if number is odd."""
    return number % 2 != 0
