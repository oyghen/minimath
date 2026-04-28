__all__ = ("identity", "dlog")

import math
from typing import Final, Literal, TypeVar, get_args

T = TypeVar("T")


_PHONE_KEYPAD_GROUPS: Final[dict[str, str]] = {
    "2": "ABC",
    "3": "DEF",
    "4": "GHI",
    "5": "JKL",
    "6": "MNO",
    "7": "PQRS",
    "8": "TUV",
    "9": "WXYZ",
}

_PHONE_KEYPAD_TRANSLATION: Final[dict[int, str]] = str.maketrans(
    {
        letter: digit
        for digit, letters in _PHONE_KEYPAD_GROUPS.items()
        for letter in letters + letters.lower()
    }
)


def phone_keypad_digits(text: str) -> str:
    """Return text with letters replaced by phone keypad digits."""
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")

    return text.translate(_PHONE_KEYPAD_TRANSLATION)


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
