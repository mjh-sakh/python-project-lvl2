#!/usr/bin/env python3

import argparse
from gendiff.generate_diff import generate_diff

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

parser = argparse.ArgumentParser(description="Compares two json objects and shows differences between them.",  # noqa: E501
                                 usage=DESCRIPTION,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("first_file", help="First file to compare.")
parser.add_argument("second_file", help="Second file to compare.")
parser.add_argument("-f", "--format", choices=['json', 'pain'], help="Set format of output. 'json' is default.")  # noqa: E501


def main():
    args = parser.parse_args()
    print(generate_diff(args.first_file, args.second_file))


if __name__ == "__main__":
    main()
