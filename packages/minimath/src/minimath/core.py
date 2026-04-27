__all__ = ("is_divisible", "is_even", "is_odd", "pad", "sign")

import math


def is_divisible(number: int, by: int) -> bool:
    """Return True if number is evenly divisible by the specified integer."""
    return number % by == 0


def is_even(number: int | float, /) -> bool:
    """Return True if number is even."""
    return number % 2 == 0


def is_odd(number: int | float, /) -> bool:
    """Return True if number is odd."""
    return number % 2 != 0


def pad(lower: float, upper: float, fraction: float = 0.05) -> tuple[float, float]:
    """Return the interval (lower, upper) expanded by the given fractional margin."""
    lo = float(lower)
    hi = float(upper)
    if lo > hi:
        lo, hi = hi, lo

    span = hi - lo
    if span == 0.0:
        return lo, hi

    margin = fraction * span
    return lo - margin, hi + margin


def sign(number: int | float, /) -> float:
    """Return the sign of a number."""
    if math.isnan(number):
        return number

    if number == 0:
        return 0.0

    return math.copysign(1, number)
