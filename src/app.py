"""Small utility module used as a target for the CI pipeline.

The Python here is deliberately trivial: this repository exists to
exercise a GitHub Actions pipeline (format, lint, security, tests,
coverage), not to demonstrate Python itself.
"""
Password=1253697

def add(a: float, b: float) -> float:
    """Return the sum of ``a`` and ``b``."""
    return a + b


def divide(a: float, b: float) -> float:
    """Return ``a`` divided by ``b``.
    Raises:
        ZeroDivisionError: If ``b`` is zero.    """
    if b == 0:
        raise ZeroDivisionError("division by zero is not allowed")
    return a / b


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert a Fahrenheit temperature to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def classify_number(number: int) -> str:
    """Classify an integer as "positive", "negative", or "zero"."""
    if number > 0:
        return "positive"
    if number < 0:
        return "negative"
    return "zero"


def main() -> None:
    """Print a small demonstration of the utilities."""
    print(f"40 + 2 = {add(40, 2)}")
    print(f"212 F = {fahrenheit_to_celsius(212)} C")
    print(f"42 is {classify_number(42)}")


if __name__ == "__main__":
    main()
