import minimath


def main() -> None:
    result = minimath.__name__
    expected = "minimath"
    if result == expected:
        print(f"Smoke test for {minimath.__name__}: PASSED")
    else:
        raise RuntimeError(f"Smoke test for {minimath.__name__}: FAILED")


if __name__ == "__main__":
    main()
