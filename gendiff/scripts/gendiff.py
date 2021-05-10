#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Generate diff.")
parser.add_argument("first_file", help="First file to compare.")
parser.add_argument("second_file", help="Second file to compare.")
parser.add_argument("-f", "--format", help="Set format of output.")

def main():
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
