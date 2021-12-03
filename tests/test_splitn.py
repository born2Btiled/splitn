from typer.testing import CliRunner
from random import seed

from splitn.main import app

runner = CliRunner()

seed(0)

OUTPUT_3 = '123\n1 23\n12 3\n1 2 3'
OUTPUT_2 = '45\n4 5'
OUTPUT_PATTERN = '42\n4 2'
OUTPUT_SEPARATOR = '123\n1-23\n12-3\n1-2-3'

# '123\n1 23\n12 3\n1 2 3\n45\n4 5'


def test_one_operand():
    result = runner.invoke(app, ['123'])
    assert result.exit_code == 0
    for produced, expected in zip(result.stdout, OUTPUT_3):
        assert produced == expected

def test_two_operands():
    result = runner.invoke(app, ['123', '45'])
    for produced, expected in zip(result.stdout, OUTPUT_3 + '\n\n' + OUTPUT_2):
        assert produced == expected

def test_separator():
    result = runner.invoke(app, ['--separator', '-' '123'])
    for produced, expected in zip(result.stdout, OUTPUT_SEPARATOR):
        assert produced == expected

def test_as_pattern():
    result = runner.invoke(app, ['--pattern', '\\d{2}'])
    for produced, expected in zip(result.stdout, OUTPUT_PATTERN):
        assert produced == expected

def test_times():
    result = runner.invoke(app, ['--times', '2', '123'])
    for produced, expected in zip(result.stdout, OUTPUT_3 + '\n\n' + OUTPUT_3):
        assert produced == expected
