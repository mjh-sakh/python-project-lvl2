import os

from gendiff.data_type import Comparisons, FLAGS
from gendiff import formatter_stylish
from gendiff import formatter_plain
from gendiff import formatter_json
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


def prepare_value_for_comparisons(value):
    """
    Check if value is dict and convert it to Comparisons for better handling.

    :param value: any.
    :return: Comparisons or value itself.
    """
    if type(value) == dict:
        return get_comparison_for_two_dicts(value, value)
    return value


def get_comparison_for_two_dicts(dict1: dict, dict2: dict):
    """
    Compare two dictionaries and write all differences in Comparisons list.

    :param dict1: first dict.
    :param dict2: second dict.
    :return: Comparisons class.
    """

    keys1 = dict1.keys()
    keys2 = dict2.keys()
    all_keys = keys1 | keys2
    comparisons = Comparisons()
    for key in sorted(list(all_keys)):
        if key not in dict1:  # key only in dict2
            flag = FLAGS["new"]
            value = dict2[key]
            value = prepare_value_for_comparisons(value)
            comparisons.add_item(flag, key, value)
        elif key not in dict2:  # key only in dict1
            flag = FLAGS["removed"]
            value = dict1[key]
            value = prepare_value_for_comparisons(value)
            comparisons.add_item(flag, key, value)
        else:
            value1 = dict1[key]
            value2 = dict2[key]
            if value1 == value2:
                flag = FLAGS["unchanged"]
                value = prepare_value_for_comparisons(value1)
                comparisons.add_item(flag, key, value)
            elif type(value1) == dict and type(value2) == dict:
                flag = FLAGS["unchanged"]
                sub_comparisons = get_comparison_for_two_dicts(value1, value2)
                comparisons.add_item(flag, key, sub_comparisons)
            else:
                flag = FLAGS["changed_old"]
                value1 = value = prepare_value_for_comparisons(value1)
                comparisons.add_item(flag, key, value1)
                flag = FLAGS["changed_new"]
                value2 = value = prepare_value_for_comparisons(value2)
                comparisons.add_item(flag, key, value2)
    return comparisons
