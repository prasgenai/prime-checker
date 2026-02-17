import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_DIR = Path(__file__).parent

from prime_checker import is_prime, format_result, parse_input, interactive_mode


# --- is_prime() unit tests ---

@pytest.mark.parametrize("n, expected", [
    (2, True),
    (3, True),
    (17, True),
    (4, False),
    (20, False),
    (1, False),
    (0, False),
    (-5, False),
])
def test_is_prime(n, expected):
    assert is_prime(n) == expected


# --- parse_input() tests ---

@pytest.mark.parametrize("text, expected_n", [
    ("7", 7),
    ("-5", -5),
    ("0", 0),
])
def test_parse_input_numeric(text, expected_n):
    n, label = parse_input(text)
    assert n == expected_n
    assert label == str(expected_n)


@pytest.mark.parametrize("text, expected_n", [
    ("two", 2),
    ("three", 3),
    ("seventeen", 17),
    ("four", 4),
    ("twenty", 20),
    ("thirty one", 31),
    ("minus five", -5),
    ("TWO", 2),
    ("Two", 2),
])
def test_parse_input_words(text, expected_n):
    n, label = parse_input(text)
    assert n == expected_n
    assert label == text.strip()


@pytest.mark.parametrize("text", ["fox", "hello", "abc"])
def test_parse_input_invalid(text):
    with pytest.raises(ValueError):
        parse_input(text)


# --- format_result() tests ---

def test_format_result_prime():
    assert format_result(7) == "7 is a prime integer"


def test_format_result_not_prime():
    assert format_result(10) == "10 is NOT a prime integer"


def test_format_result_with_label():
    assert format_result(2, "two") == "two is a prime integer"
    assert format_result(4, "four") == "four is NOT a prime integer"


# --- CLI tests ---

def test_cli_prime():
    result = subprocess.run(
        [sys.executable, "prime_checker.py", "7"],
        capture_output=True, text=True,
        cwd=PROJECT_DIR,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "7 is a prime integer"


def test_cli_not_prime():
    result = subprocess.run(
        [sys.executable, "prime_checker.py", "10"],
        capture_output=True, text=True,
        cwd=PROJECT_DIR,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "10 is NOT a prime integer"


def test_cli_invalid_input():
    result = subprocess.run(
        [sys.executable, "prime_checker.py", "abc"],
        capture_output=True, text=True,
        cwd=PROJECT_DIR,
    )
    assert result.returncode != 0
    assert result.stderr.strip() != ""


def test_cli_word_prime():
    result = subprocess.run(
        [sys.executable, "prime_checker.py", "two"],
        capture_output=True, text=True,
        cwd=PROJECT_DIR,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "two is a prime integer"


def test_cli_word_not_prime():
    result = subprocess.run(
        [sys.executable, "prime_checker.py", "twenty"],
        capture_output=True, text=True,
        cwd=PROJECT_DIR,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "twenty is NOT a prime integer"


def test_cli_word_invalid():
    result = subprocess.run(
        [sys.executable, "prime_checker.py", "fox"],
        capture_output=True, text=True,
        cwd=PROJECT_DIR,
    )
    assert result.returncode != 0
    assert result.stderr.strip() != ""


# --- interactive_mode() unit tests ---

def test_interactive_prime_then_quit(monkeypatch, capsys):
    inputs = iter(["7", "quit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    interactive_mode()
    output = capsys.readouterr().out
    assert "7 is a prime integer" in output
    assert "Goodbye!" in output


def test_interactive_not_prime_then_quit(monkeypatch, capsys):
    inputs = iter(["10", "quit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    interactive_mode()
    output = capsys.readouterr().out
    assert "10 is NOT a prime integer" in output
    assert "Goodbye!" in output


def test_interactive_invalid_then_valid_then_quit(monkeypatch, capsys):
    inputs = iter(["abc", "7", "quit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    interactive_mode()
    output = capsys.readouterr().out
    assert "Error:" in output
    assert "7 is a prime integer" in output
    assert "Goodbye!" in output


def test_interactive_word_input_then_quit(monkeypatch, capsys):
    inputs = iter(["two", "quit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    interactive_mode()
    output = capsys.readouterr().out
    assert "two is a prime integer" in output
    assert "Goodbye!" in output


def test_interactive_immediate_quit(monkeypatch, capsys):
    inputs = iter(["quit"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    interactive_mode()
    output = capsys.readouterr().out
    assert "Goodbye!" in output
    assert "prime" not in output.lower().replace("goodbye!", "")


def test_interactive_case_insensitive_quit(monkeypatch, capsys):
    for cmd in ["QUIT", "Q", "Exit"]:
        inputs = iter([cmd])
        monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
        interactive_mode()
        output = capsys.readouterr().out
        assert "Goodbye!" in output


# --- CLI interactive integration test ---

def test_cli_interactive_mode():
    result = subprocess.run(
        [sys.executable, "prime_checker.py"],
        input="7\nquit\n",
        capture_output=True, text=True,
        cwd=PROJECT_DIR,
    )
    assert result.returncode == 0
    assert "7 is a prime integer" in result.stdout
    assert "Goodbye!" in result.stdout
