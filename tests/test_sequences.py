from utils import sequences
from random import seed

INPUT = "\\d[a-d]{4,7}"
OUTPUT = "6acddcdc"

def test_random_sequence():
    seed(0)
    assert sequences.random_sequence("\\d[a-d]{4,7}") == OUTPUT

