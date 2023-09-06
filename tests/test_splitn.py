from unittest import result
from typer.testing import CliRunner
from random import seed

from splitn.main import app

runner = CliRunner()

INPUT_1 = "123"
OUTPUT_1 = "123\n1 23\n12 3\n1 2 3\n"

INPUT_2 = "\\\\d{2}"
OUTPUT_2 = "60\n6 0\n"

INPUT_3 = "\\d{2}"
OUTPUT_3 = "87\n8 7\n"

SEPARATOR = "-"
OUTPUT_SEPARATOR = "123\n1-23\n12-3\n1-2-3\n"

PATTERN = "\\d{2} \\d"
OUTPUT_4 = "47 5\n"
OUTPUT_5 = "12 3\n"

def test_app() -> None:
    seed(0)
    result = runner.invoke(app, INPUT_1)
    assert result.exit_code == 0
    assert result.stdout == OUTPUT_1

def test_regex() -> None:
    seed(0)
    result = runner.invoke(app, str(INPUT_2))
    assert result.stdout == OUTPUT_2
    
def test_two_operands() -> None:
    seed(0)
    result = runner.invoke(app, [INPUT_1, INPUT_3])
    assert result.stdout == OUTPUT_1 + "---\n" + OUTPUT_2

def test_separator() -> None:
    seed(0)
    result = runner.invoke(app, ["--separator", SEPARATOR, INPUT_1])
    assert result.stdout == OUTPUT_SEPARATOR

def test_times() -> None:
    seed(0)
    result = runner.invoke(app, ["--times", "2", INPUT_3])
    assert result.stdout == OUTPUT_2 + "\n" + OUTPUT_3

def test_pattern() -> None:
    result = runner.invoke(app, ["--pattern", PATTERN])
    assert result.stdout == OUTPUT_4

def test_pattern_with_operand() -> None:
    result = runner.invoke(app, [INPUT_1, "--pattern", PATTERN])
    assert result.stdout == OUTPUT_5
