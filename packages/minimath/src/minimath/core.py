__all__ = ("collatz", "fibonacci", "is_divisible", "is_even", "is_odd")

from collections.abc import Iterator


def collatz(n: int, /) -> Iterator[int]:
    """Return the Collatz sequence."""
    if not isinstance(n, int):
        raise TypeError(f"unsupported type {type(n).__name__!r}; expected int")
    if n < 1:
        raise ValueError(f"invalid value {n!r}; expected >= 1")

    while True:
        yield n
        if n == 1:
            break
        n = n // 2 if is_even(n) else 3 * n + 1


def fibonacci(a: int = 0, b: int = 1, /) -> Iterator[int]:
    """Return the Fibonacci sequence."""
    yield a
    yield b
    while True:
        c = a + b
        yield c
        a, b = b, c


def is_divisible(number: int, by: int) -> bool:
    """Return True if number is evenly divisible by the specified integer."""
    return number % by == 0


def is_even(number: int | float, /) -> bool:
    """Return True if number is even."""
    return number % 2 == 0


def is_odd(number: int | float, /) -> bool:
    """Return True if number is odd."""
    return number % 2 != 0
