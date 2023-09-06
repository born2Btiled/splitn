import sys
from typing import Iterator, Generator
from itertools import combinations, chain

def split_sequences(sequence: str, separator: str = ' ') -> Generator[str, None, None]:
    for pattern in patterns(len(sequence)):
        yield split(sequence=sequence, pattern=pattern, separator=separator)

def patterns(length: int) -> Iterator[tuple[int, ...]]:
    return chain.from_iterable((combinations(range(length - 1), k) for k in range(length)))

def split(sequence: str, pattern: tuple[int, ...], separator: str) -> str:
    combination = []
    l = 0
    for r in (pos + 1 for pos in pattern):
        combination.append(sequence[l:r])
        combination.append(separator)
        l = r
    combination.append(sequence[l:])
    return "".join(combination)

def main() -> str | int:
    try:
        for sequence in split_sequences(str(sys.argv[1])):
            print(sequence)
    except:
        return 1

if __name__ == "__main__":
    sys.exit(main())
