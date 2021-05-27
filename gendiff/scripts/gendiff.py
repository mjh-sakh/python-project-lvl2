#!/usr/bin/env python3

from gendiff import generate_diff
from gendiff.arg_parse import get_parser


def main():
    """
    Parse gendiff args and print comparison results.
    """
    parser = get_parser()
    args = parser.parse_args()
    print(generate_diff(args.first_file,
                        args.second_file,
                        formatter=args.format))


if __name__ == "__main__":
    main()
