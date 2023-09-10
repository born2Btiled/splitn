import argparse
from sys import argv
from os import path
from re import fullmatch
from itertools import tee

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from typing import Generator

from loguru import logger

from utils.sequences import random_sequence
from utils.split import split_sequences

VERSION = "3.2.0"

DESCRIPTION = """
[underline]splitn[/underline] - a CLI application that generates combinations of chars being a result of splitting strings
"""

USAGE = """
[yellow]Usage:[/yellow]  [b]splitn \\[options] \\[strings... | regexes... | files...]
        splitn \\[options] \\[strings... | regexes... | files...] --pattern | -p <regexes...>
        splitn \\[--times <integer>] \\[--secondary-separator <string>] --pattern | -p <regexes...>[/b]"""

EXAMPLE = """
$ splitn abc "\\d{2}"
abc
a bc
ab c
a b c
---
60
6 0"""

EPILOG = "For options, use 'splitn --help'."

ARGUMENTS = Table(box=None)
ARGUMENTS.add_column(justify="left")
ARGUMENTS.add_column(justify="left", style="yellow")
ARGUMENTS.add_column(justify="left")
ARGUMENTS.add_row(
    "operands",
    "\\[strings... | regexes... | files...]",
    "List of strings, regular expressions or files.\nProvided files should contain a list of strings or regular expressions.\nRegular expressions should have \"\\\" escaped (eg. \"\\d\") or be inside quotes.\nGiven operands are treated as regular expressions by default."
)

OPTIONS = Table(box=None)
OPTIONS.add_column(justify="left", style="green")
OPTIONS.add_column(justify="left", style="cyan")
OPTIONS.add_column(justify="left", style="yellow")
OPTIONS.add_column(justify="left")
OPTIONS.add_row(
    "-s",
    "--separator",
    "<string>",
    "Separator used in splitting generated sequences. \\[default:' ']"
)
OPTIONS.add_row(
    "-t",
    "--times",
    "<int>",
    "Number of times splitn generates sequences for each specification. Applied only for regular expressions. \\[default: 1]"
)
OPTIONS.add_row(
    "",
    "--secondary-separator",
    "<string>",
    "Separator used to separate outputs from different provided specifications. Use empty string for having new line. \\[default: ---]"
)
OPTIONS.add_row(
    "",
    "--as-string",
    "",
    "Interpret provided operands as simple strings."
)
OPTIONS.add_row(
    "-p",
    "--pattern",
    "<regexes...>",
    "Use this option to either generate random sequence from regular expressions without splitting, or to narrow down sequences generated from given operands to those matching provided regular expressions. \\[default: None]"
)
OPTIONS.add_row(
    "-v",
    "--version",
    "",
    "Show version of splitn."
)
OPTIONS.add_row(
    "-h",
    "--help",
    "",
    "Show this message."
)

CONCISE_HELP = Group(
    DESCRIPTION,
    USAGE,
    "\n",
    Panel(
        EXAMPLE,
        title="Example",
        title_align="left"
    ),
    EPILOG
)

HELP = Group(
    DESCRIPTION,
    USAGE,
    "\n",
    Panel(
        ARGUMENTS,
        title="Arguments",
        title_align="left"
    ),
    Panel(
        OPTIONS,
        title="Options",
        title_align="left"
    )
)

parser = argparse.ArgumentParser(
        prog="splitn",
        usage="%(prog)s [options] [operands ...] [--pattern | -p <regexes> ...]",
        add_help=False,
        allow_abbrev=False
    )
parser.add_argument(
    "operands",
    nargs="*",
    type=str
)
parser.add_argument(
    "--separator", "-s",
    default=" ",
    type=str
)
parser.add_argument(
    "--times", "-t",
    default=1,
    type=int
)
parser.add_argument(
    "--secondary-separator",
    default="---",
    type=str
)
parser.add_argument(
    "--as-string",
    action="store_true"
)
parser.add_argument(
    "--pattern", "-p",
    nargs="*",
    default=None,
    type=str
)
parser.add_argument(
    "--version", "-v",
    action="version",
    version=f"%(prog)s {VERSION}"
)
parser.add_argument(
    "--help", "-h",
    action="store_true"
)

console = Console()

@logger.catch
def detect_string(
    input: str
) -> bool:
    try:
        return bool(fullmatch(input, input))
    except Exception:
        return False

@logger.catch
def generate_split_sequences(
    sequence: str,
    separator: str,
    patterns: list[str] | None
) -> Generator[str, None, None]:
    for split_sequence in split_sequences(sequence, separator):
        printable: bool = not patterns
        if patterns:
            for pattern in patterns:
                printable = fullmatch(pattern, split_sequence.strip())
                if printable:
                    break
        if printable:
            yield split_sequence

@logger.catch
def generate_output(
    operand: str,
    separator: str,
    times: int,
    as_string: bool,
    patterns: list[str] | None
) -> Generator[str, None, None]:
    try:
        if as_string or detect_string(operand):
            # handle simple strings
            yield from generate_split_sequences(operand, separator, patterns)
        else: 
            # handle regular expressions
            for counter in range(times):
                sequence = random_sequence(operand)
                yield from generate_split_sequences(sequence, separator, patterns)
                if counter < times - 1:
                    yield ""
    except Exception as e:
        parser.error(f"Program aborted with exception: {e}.")

@logger.catch
def handle_operands(
    operands: list[str],
    separator: str,
    times: int,
    secondary_separator: str,
    as_string: bool,
    patterns: list[str]
) -> Generator[str, None, None]:
    for operand, counter in zip(operands, range(len(operands), 0, -1)):
        if not path.exists(operand):
            yield from generate_output(operand, separator, times, as_string, patterns)
        else:
            with open(operand) as file:
                lines = file.readlines()
                for line, line_counter in zip(lines, range(len(lines), 0, -1)):
                    yield from generate_output(line.strip(), separator, times, as_string, patterns)
                    if line_counter > 1:
                        yield secondary_separator
        if counter > 1:
            yield secondary_separator

@logger.catch
def handle_pattern(
    patterns: list[str],
    times: int,
    secondary_separator: str
) -> Generator[str, None, None]:
    for pattern, counter in zip(patterns, range(len(patterns), 0, -1)):
        for _ in range(times):
            yield random_sequence(pattern)
    if counter > 1:
        yield secondary_separator

@logger.catch
def print_output(
    outputs: Generator
) -> None:
    (outputs_original, outputs_copy) = tee(outputs, 2)
    for _ in range(console.height):
        next_output = next(outputs_original, None)
        if next_output is None:
            break
    if next_output is None:
        for output in outputs_copy:
            console.print(output)
    else:
        with console.pager():
            for output in outputs_copy:
                console.print(output)

@logger.catch
def main(
    args: list[str]
) -> None:
    args = parser.parse_args(args)

    if args.help:
        console.print(HELP)
        parser.exit()

    if not args.operands and not args.pattern:
        console.print(CONCISE_HELP)
        parser.exit(1)
    
    if args.operands:
        print_output(
            handle_operands(args.operands, args.separator, args.times, args.secondary_separator, args.as_string, args.pattern)
        )
        parser.exit()
       
    if args.pattern:
        print_output(
             handle_pattern(args.pattern, args.times, args.secondary_separator)
        )
        parser.exit()

if __name__ == "__main__":
    main(argv[1:])