#!/usr/bin/env python3

import argparse
from gendiff.generate_diff import generate_diff

parser = argparse.ArgumentParser(description="Generate diff.")
parser.add_argument("first_file", help="First file to compare.")
parser.add_argument("second_file", help="Second file to compare.")
parser.add_argument("-f", "--format", help="Set format of output.")


def main():
    args = parser.parse_args()
    print(args)
    generate_diff(args.first_file, args.second_file)


if __name__ == "__main__":
    main()
