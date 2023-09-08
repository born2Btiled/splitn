import pytest
from utils import sequences
from random import seed

INPUT = "\\d[a-d]{4,7}"
OUTPUT = "6acddcdc"

def test_main(capsys) -> None:
    seed(0)
    with pytest.raises(SystemExit) as e:
        sequences.main(INPUT)
    assert e.type == SystemExit
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert captured.out == f"{OUTPUT}\n"

def test_random_sequence() -> None:
    seed(0)
    assert sequences.random_sequence(INPUT) == OUTPUT

