import os
from typing import Optional

from gendiff.comparisons_builder import get_comparisons
from gendiff.formatters.formatter import get_formatter
from gendiff.parsing import get_proper_load_to_dict
from gendiff.utilities import read_


def generate_diff(
        file1: str,
        file2: str,
        formatter: Optional[str] = 'stylish'
) -> str:
    """
    Generate comparison between two files.

    :param formatter: defines representation of result.
    :param file1: path to file 1.
    :param file2: path to file 2.
    :return: comparison string in json-like format.
    """
    assert os.path.isfile(file1), f"{file1} is not a file."
    assert os.path.isfile(file2), f"{file2} is not a file."
    formatter = 'stylish' if formatter is None else formatter

    load_to_dict = get_proper_load_to_dict(file1)
    dict1 = load_to_dict(read_(file1))
    load_to_dict = get_proper_load_to_dict(file2)
    dict2 = load_to_dict(read_(file2))
    comparisons = get_comparisons(dict1, dict2)
    generate_comparison_output_string = get_formatter(formatter)
    comparisons_string = generate_comparison_output_string(comparisons)
    return comparisons_string
