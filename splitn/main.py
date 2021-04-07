from itertools import chain, combinations, repeat
from collections.abc import Generator
from copy import deepcopy
from random import randint
from re import compile

import typer

class CombinationsGenerator():
    def __init__(self, seed: str, separator: str) -> None:
        self.seed = seed
        self.separator = separator
        self.length = len(self.seed)
        self.digits = [digit for digit in self.seed]

    def combinations(self) -> Generator[str, None, None]:
        for k in range(0, self.length):
            if not k:
                yield self.seed
            else:
                for pattern in combinations(range(1, self.length), k):
                    yield self.split_n(pattern)

    def split_n(self, pattern: tuple[int, ...]) -> str:
        combination = deepcopy(self.digits)
        for position, i in zip(pattern, range(len(pattern))):
            combination.insert(position + i, self.separator)
        return "".join(combination)

class RandomNumbersGenerator():
    def __init__(self, length:int) -> None:
        self.length = length

    def random_number(self) -> str:
        return "".join([str(randint(0,9)) for _ in repeat(None, self.length)])


app = typer.Typer()

@app.command()
def main(operands: list[str] = typer.Argument(None,
                                              help="Each operand can be an integer or a range of integers written as 'L..R', where L and R are respectively left and right end of a range. Each integer defines length of randomly generated sequence of digits. For example, calling 'splitn 2..5' will produce four random sequences consisted of 2,3,4 and 5 digits and every combination being a result of splitting these digits."),
         separator: str = typer.Option(" ",
                                       "--separator", "-s",
                                       help="Separator used in splitting generated sequences"),
         random: bool = typer.Option(False,
                                     "--random-only", "-r",
                                     help="Avoid splitting generated sequences"),
         times: int = typer.Option(1,
                                   "--times", "-t",
                                   help="Number of times splitn should generate sequences according to provided specification")):
    
    input = chain()
    range_pattern = compile(r"^(\d+)\.+(\d+)$")
    for operand in operands:
        if not operand.isdigit():
            match = range_pattern.match(operand)
            if match:
                left = int(match.group(1))
                right = int(match.group(2))
                if left <= right:
                    for o in range(left, right + 1):
                        input = chain(input, [o])
                else:
                    exit("Error: Invalid value for operand: in range '{}' left end is bigger then right end")
            else:
                exit("Error: Invalid value for operand: '{}' is not a valid integer or range of integers".format(operand))
        else:
            input = chain(input, [operand])

    output = chain()
    number = new_number = ''
    for operand in input:
        for _ in repeat(None, times):
            while new_number == number:
                new_number = RandomNumbersGenerator(int(operand)).random_number()
            number = new_number 
            output = chain(output,
                          [number] if random else CombinationsGenerator(number, separator).combinations())

    for line in output:
        typer.echo(line)

if __name__ == "__main__":
    app()
