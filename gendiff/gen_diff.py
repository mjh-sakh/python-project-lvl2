import os
from typing import Any, List, Dict, Optional, Callable

from gendiff.formatters import formatter_json
from gendiff.formatters import formatter_plain
from gendiff.formatters import formatter_stylish
# from gendiff.parsing import get_proper_read_to_dict_for_file
from gendiff.parsing import get_proper_read_to_dict_for_text


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
    comparisons = get_comparison_for_two_dicts(dict1, dict2)
    generate_comparison_output_string = get_formatter(formatter)
    comparisons_string = generate_comparison_output_string(comparisons)
    return comparisons_string


def read_text_from_file(file_path: str) -> str:
    """
    Open file, read it and return text.
    """
    with open(file_path, 'r') as file:
        text = file.read()
    return text


def get_formatter(formatter: str) -> Callable:
    """
    Get proper formatter function to generate string.

    :param formatter: stylish, plain or json, str.
    :return: formatter function.
    """
    if formatter == 'stylish':
        return formatter_stylish.generate_comparison_output_string
    elif formatter == "plain":
        return formatter_plain.generate_comparison_output_string
    elif formatter == "json":
        return formatter_json.generate_comparison_output_string
    else:
        raise NotImplementedError('Formatter "{formatter}" is not implemented. Choose "stylish"')  # noqa: E501


def get_comparison_for_two_dicts(  # noqa: C901
        dict1: Dict,
        dict2: Dict
) -> List[Dict[str, Any]]:
    """
    Compare two dictionaries and write all differences in comparison list.

    :param dict1: first dict.
    :param dict2: second dict.
    :return: comparisons, List[Dict[str, Any]].
    """

    def _add_item(_value, item_type):
        item = dict(key=key, item_type=item_type, value=_value)
        comparisons.append(item)

    keys1 = dict1.keys()
    keys2 = dict2.keys()
    all_keys = keys1 | keys2
    comparisons: List[Dict[str, Any]] = []
    for key in sorted(all_keys):
        value1 = dict1.get(key)
        value2 = dict2.get(key)
        if key not in dict1:  # key only in dict2
            _add_item(value2, item_type="new")
        elif key not in dict2:  # key only in dict1
            _add_item(value1, item_type="removed")
        elif value1 == value2:
            _add_item(value1, item_type="same")
        elif isinstance(value1, dict) and isinstance(value2, dict):
            sub_comparisons = get_comparison_for_two_dicts(value1, value2)
            _add_item(sub_comparisons, item_type="updated_branch")
        else:
            _add_item(value1, item_type="updated_old")
            _add_item(value2, item_type="updated_new")
    return comparisons
