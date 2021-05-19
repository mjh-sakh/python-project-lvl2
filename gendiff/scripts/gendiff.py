#!/usr/bin/env python3

import argparse

from gendiff.core import generate_diff

DESCRIPTION = r"""
  files:
    file_one: {"key1": 1, "key2" : 2}
    file_two: {"key1": 10, "key3" : 3}
   
  run command: 
    gendiff file_one file_two
    
  result:
    {
      - key1: 1,
      + key1: 10,
        key2: 2,
      + key3: 3
    }
"""  # noqa: W291, W293


def main():
    """
    Parse gendiff args and print comparison results.
    """
    parser = argparse.ArgumentParser(
        description="Compares two json objects and shows differences between them.",  # noqa: E501
        usage=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("first_file", help="First file to compare.")
    parser.add_argument("second_file", help="Second file to compare.")
    parser.add_argument("-f", "--format", choices=['stylish', 'plain', 'json'],
                        help="Set format of output. 'stylish' is default.")  # noqa: E501
    args = parser.parse_args()
    print(generate_diff(args.first_file,
                        args.second_file,
                        formatter=args.format))


if __name__ == "__main__":
    main()
