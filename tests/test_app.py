"""Unit tests for the app module."""

import pytest

from app import add, classify_number, divide, fahrenheit_to_celsius, main


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_add_floats():
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_divide():
    assert divide(10, 4) == 2.5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


def test_fahrenheit_to_celsius():
    assert fahrenheit_to_celsius(212) == pytest.approx(100)
    assert fahrenheit_to_celsius(32) == pytest.approx(0)


def test_classify_number():
    assert classify_number(42) == "positive"
    assert classify_number(-7) == "negative"
    assert classify_number(0) == "zero"


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "42" in out
