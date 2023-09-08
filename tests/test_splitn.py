import pytest
from random import seed
from splitn.main import main

INPUT_1 = "123"
OUTPUT_1 = "123\n1 23\n12 3\n1 2 3\n"

INPUT_2 = "\\d{2}"
OUTPUT_2 = "60\n6 0\n"

SECONDARY_SEPARATOR = "---\n"
OUTPUT_3 = "87\n8 7\n"

SEPARATOR = "-"
OUTPUT_4 = "123\n1-23\n12-3\n1-2-3\n"

PATTERN = "\\d{2} \\d"
OUTPUT_5 = "47 5\n"

OUTPUT_6 = "12 3\n"

def test_main(capsys) -> None:
    seed(0)
    with pytest.raises(SystemExit) as e:
        main([INPUT_1])
    assert e.type == SystemExit
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert captured.out == OUTPUT_1

def test_regex(capsys) -> None:
    seed(0)
    with pytest.raises(SystemExit) as e:
        main([INPUT_2])
    captured = capsys.readouterr()
    assert captured.out == OUTPUT_2
    
def test_two_operands(capsys) -> None:
    seed(0)
    with pytest.raises(SystemExit) as e:
        main([INPUT_1, INPUT_2])
    captured = capsys.readouterr()
    assert captured.out == f"{OUTPUT_1}{SECONDARY_SEPARATOR}{OUTPUT_2}"

def test_separator(capsys) -> None:
    with pytest.raises(SystemExit) as e:
        main(["--separator", SEPARATOR, INPUT_1])
    captured = capsys.readouterr()
    assert captured.out == OUTPUT_4

def test_times(capsys) -> None:
    seed(0)
    with pytest.raises(SystemExit) as e:
        main(["--times", "2", INPUT_2])
    captured = capsys.readouterr()
    assert captured.out == f"{OUTPUT_2}\n{OUTPUT_3}"

def test_pattern(capsys) -> None:
    with pytest.raises(SystemExit) as e:
        main(["--pattern", PATTERN])
    captured = capsys.readouterr()
    assert captured.out == OUTPUT_5

def test_pattern_with_operand(capsys) -> None:
    with pytest.raises(SystemExit) as e:
        main([INPUT_1, "--pattern", PATTERN])
    captured = capsys.readouterr()
    assert captured.out == OUTPUT_6
