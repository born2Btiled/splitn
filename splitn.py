#!/usr/bin/env python3

"""splitn

Usage:
    splitn [-s SEP] <number>
    splitn --version
    splitn -h

Options:
    -s SEP --separator=SEP  Choose separator [default:  ]
    -h --help               Show this screen
    --version               Show version
"""

from docopt import docopt
from itertools import combinations


def split(number, separator):
    print(number)
    n = len(number)
    for k in range(1, n):
        for combination in combinations(range(n-1), k):
            new_number = []
            begin = 0
            for position in combination:
                new_number.append(number[begin:position+1])
                begin = position + 1
            new_number.append(number[position+1:])
            print(str(separator).join(new_number))

            " ".join

def main():
    arguments = docopt(__doc__, version='1.1.0')
    number = arguments['<number>']
    separator = arguments['--separator']
    split(number, separator)

if __name__ == "__main__":
    main()
