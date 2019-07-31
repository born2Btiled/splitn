#!/usr/bin/env python3

import argparse
from itertools import combinations


def split(number):
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
            print(" ".join(new_number))

            " ".join

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('number', metavar='N', type=str, help='Number to split')
    args = parser.parse_args()

    number = args.number

    split(number)

if __name__ == "__main__":
    main()
