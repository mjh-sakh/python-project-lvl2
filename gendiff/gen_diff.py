import os
from typing import Optional

from gendiff.comparisons_builder import get_comparisons
from gendiff.formatters.formatter import get_formatter
# from gendiff.parsing import get_proper_read_to_dict_for_file
from gendiff.parsing import get_proper_read_to_dict_for_text
from gendiff.utilities import read_text_from_file


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

    # read_to_dict = get_proper_read_to_dict_for_file(file1)
    # dict1 = read_to_dict(file1)
    file1_text = read_text_from_file(file1)
    read_to_dict = get_proper_read_to_dict_for_text(file1_text)
    dict1 = read_to_dict(file1_text)
    # read_to_dict = get_proper_read_to_dict_for_file(file2)
    # dict2 = read_to_dict(file2)
    file2_text = read_text_from_file(file2)
    read_to_dict = get_proper_read_to_dict_for_text(file2_text)
    dict2 = read_to_dict(file2_text)
    comparisons = get_comparisons(dict1, dict2)
    generate_comparison_output_string = get_formatter(formatter)
    comparisons_string = generate_comparison_output_string(comparisons)
    return comparisons_string


