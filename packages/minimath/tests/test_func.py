import copy
from typing import Any

import minimath
import pytest


class TestPhoneKeypadDigits:
    @pytest.mark.parametrize(
        ("input_text", "expected"),
        [
            ("ABC", "222"),
            ("def", "333"),
            ("Hello", "43556"),
            ("WORLD", "96753"),
            ("Call Me", "2255 63"),
            ("1-800-FLOWERS", "1-800-3569377"),
            ("minimath", "64646284"),
            ("Hello, World!", "43556, 96753!"),
        ],
    )
    def test_basic_letter_conversion(self, input_text: str, expected: str) -> None:
        assert minimath.func.phone_keypad_digits(input_text) == expected

    @pytest.mark.parametrize(
        "input_text",
        [
            "",
            "12345",
            "1-2-3",
            "   ",
            "!@#$%",
        ],
    )
    def test_non_letters_are_preserved(self, input_text: str) -> None:
        assert minimath.func.phone_keypad_digits(input_text) == input_text

    @pytest.mark.parametrize(
        ("input_text", "expected"),
        [
            ("aBcDeF", "222333"),
            ("PyThOn", "798466"),
        ],
    )
    def test_case_insensitivity(self, input_text: str, expected: str) -> None:
        assert minimath.func.phone_keypad_digits(input_text) == expected

    @pytest.mark.parametrize(
        "invalid_input",
        [
            None,
            123,
            12.34,
            ["ABC"],
            {"text": "ABC"},
        ],
    )
    def test_invalid_input_type_raises(self, invalid_input) -> None:
        with pytest.raises(TypeError):
            minimath.func.phone_keypad_digits(invalid_input)


@pytest.mark.parametrize(
    "value, is_mutable",
    [
        (None, False),
        (5, False),
        ("abc", False),
        ([1, 2, 3], True),
        ((1, 2), False),
        ({"a": 1}, True),
    ],
)
def test_identity(value: Any, is_mutable: bool):
    expected = copy.deepcopy(value)

    result = minimath.func.identity(value)

    assert result is value
    assert result == expected
    if is_mutable:
        assert result is not expected


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
            result = minimath.func.dlog(v)
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
            result = minimath.func.dlog(v, kind="int")
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
            result = minimath.func.dlog(v, kind="linear")
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
            result = minimath.func.dlog(v)
            assert isinstance(result, float)
            assert result == expected

    @pytest.mark.parametrize("kind", [None, "LOG", 1, 2.0, "invalid_kind"])
    def test_invalid_values(self, kind: str):
        with pytest.raises(ValueError):
            minimath.func.dlog(10, kind=kind)  # type: ignore
