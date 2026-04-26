import minimath_cli


def main():
    result = minimath_cli.__name__
    expected = "minimath_cli"
    if result == expected:
        print(f"Smoke test for {minimath_cli.__name__}: PASSED")
    else:
        raise RuntimeError(f"Smoke test for {minimath_cli.__name__}: FAILED")


if __name__ == "__main__":
    main()
