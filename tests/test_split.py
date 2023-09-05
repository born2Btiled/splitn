from utils import split

SEQUENCE = "123"
PATTERN = (0, 1)
SEPARATOR = "-"
OUTPUT = "1-2-3"
PATTERNS = (
    (),
    (0,),
    (1,),
    (0,1)
)

def test_split():
    assert split.split(SEQUENCE, PATTERN, SEPARATOR) == OUTPUT

def test_patterns():
    for produced, expected in zip(split.patterns(3), PATTERNS):
        assert produced == expected
