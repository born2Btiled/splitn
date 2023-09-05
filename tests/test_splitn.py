from typer.testing import CliRunner
from random import seed

from ..splitn.main import app

runner = CliRunner()

INPUT_1 = "123"
OUTPUT_1 = "123\n1 23\n12 3\n1 2 3\n"

INPUT_2 = "\\\\d{2}"
OUTPUT_2 = "60\n6 0\n"

INPUT_3 = "\\d{2}"
OUTPUT_3 = "87\n8 7\n"

OUTPUT_SEPARATOR = '123\n1-23\n12-3\n1-2-3\n'

def test_app():
    seed(0)
    result = runner.invoke(app, INPUT_1)
    assert result.exit_code == 0
    assert result.stdout == OUTPUT_1

def test_regex():
    seed(0)
    result = runner.invoke(app, str(INPUT_2))
    assert result.stdout == OUTPUT_2
    
def test_two_operands():
    seed(0)
    result = runner.invoke(app, [INPUT_1, INPUT_3])
    assert result.stdout == OUTPUT_1 + "---\n" + OUTPUT_2

def test_separator():
    seed(0)
    result = runner.invoke(app, ["--separator", "-", INPUT_1])
    assert result.stdout == OUTPUT_SEPARATOR

def test_times():
    seed(0)
    result = runner.invoke(app, ["--times", "2", INPUT_3])
    assert result.stdout == OUTPUT_2 + "\n" + OUTPUT_3
