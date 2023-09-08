import pytest
from utils import split

INPUT_1 = "123"
SEPARATOR = "-"
OUTPUT_1 = "123\n1-23\n12-3\n1-2-3\n"
PATTERN = (0, 1)
OUTPUT_2 = "1-2-3"
PATTERNS = (
    (),
    (0,),
    (1,),
    (0,1)
)

def test_main(capsys) -> None:
    with pytest.raises(SystemExit) as e:
        split.main(INPUT_1, SEPARATOR)
    assert e.type == SystemExit
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert captured.out == OUTPUT_1

def test_split() -> None:
    assert split.split(INPUT_1, PATTERN, SEPARATOR) == OUTPUT_2

def test_patterns() -> None:
    for produced, expected in zip(split.patterns(3), PATTERNS):
        assert produced == expected
