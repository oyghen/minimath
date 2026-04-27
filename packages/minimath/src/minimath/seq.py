__all__ = ("collatz", "fibonacci")

from collections.abc import Iterator

from minimath.core import is_even


def collatz(n: int, /) -> Iterator[int]:
    """Return the Collatz sequence."""
    if not isinstance(n, int):
        raise TypeError(f"expected int, got {type(n).__name__}")
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
