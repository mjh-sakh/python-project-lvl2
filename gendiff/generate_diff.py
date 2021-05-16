import os
from typing import Any, List, Dict

from gendiff import formatter_json
from gendiff import formatter_plain
from gendiff import formatter_stylish
from gendiff.parsing import get_proper_read_to_dict_for_file


def generate_diff(file1: str, file2: str, formatter: str = 'stylish') -> str:
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

    read_to_dict = get_proper_read_to_dict_for_file(file1)
    dict1 = read_to_dict(file1)
    read_to_dict = get_proper_read_to_dict_for_file(file2)
    dict2 = read_to_dict(file2)
    comparisons = get_comparison_for_two_dicts(dict1, dict2)
    if formatter == 'stylish':
        comparisons_string = formatter_stylish.generate_comparison_output_string(comparisons)  # noqa: E501
    elif formatter == "plain":
        comparisons_string = formatter_plain.generate_comparison_output_string(comparisons)  # noqa: E501
        if comparisons_string:
            comparisons_string = comparisons_string[:-1]  # removing last \n
    elif formatter == "json":
        comparisons_string = formatter_json.generate_comparison_output_string(comparisons)  # noqa: E501
    else:
        assert False, f'Formatter "{formatter}" is not implemented. Choose "stylish"'  # noqa: E501
    return comparisons_string


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
        if type(_value) == dict:
            node_type = "branch"
            _value = get_comparison_for_two_dicts(_value, _value)
        else:
            node_type = "leaf"
        item = dict(key=key, item_type=item_type, node_type=node_type, value=_value)  # noqa: E501
        comparisons.append(item)

    keys1 = dict1.keys()
    keys2 = dict2.keys()
    all_keys = keys1 | keys2
    comparisons = []
    item_type: str
    value: Any
    for key in sorted(list(all_keys)):
        if key not in dict1:  # key only in dict2
            value = dict2[key]
            _add_item(value, item_type="new")
        elif key not in dict2:  # key only in dict1
            value = dict1[key]
            _add_item(value, item_type="removed")
        else:
            value1 = dict1[key]
            value2 = dict2[key]
            if value1 == value2:
                _add_item(value1, item_type="same")
            elif type(value1) == dict and type(value2) == dict:
                sub_comparisons = get_comparison_for_two_dicts(value1, value2)
                item = dict(key=key, item_type="same", node_type="branch", value=sub_comparisons)  # noqa: E501
                comparisons.append(item)
            else:
                _add_item(value1, item_type="updated_old")
                _add_item(value2, item_type="updated_new")
    return comparisons
