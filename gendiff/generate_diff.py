import os
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

    read_to_dict = get_proper_read_to_dict_for_file(file1)
    dict1 = read_to_dict(file1)
    read_to_dict = get_proper_read_to_dict_for_file(file2)
    dict2 = read_to_dict(file2)
    comparisons = get_comparison_for_two_dicts(dict1, dict2)
    if formatter == 'stylish':
        comparisons_string = generate_comparison_output_string(comparisons)
    else:
        assert False, f'Formatter "{formatter}" is not implemented. Choose "stylish"'  # noqa: E501
    return comparisons_string


class Comparisons(list):
    """
    Container to store per-value comparisons based on list.
    Provides two methods on top of list type:
      add_item: adds tuple to the list (flag, key, value)
      convert_value_to_string: converts all values to strings
    """

    def __init__(self):
        super().__init__()

    def add_item(self, flag, key, value):
        """
        Add comparison item into list.

        :param flag: +/- or empty, str.
        :param key: str.
        :param value: original value, that will be converted to str.
        """
        self.append((flag, key, value))

    # def __getitem__(self, item):
    #     return dict(zip(["flag", "key", "value"], super().__getitem__(item)))


def convert_value_to_string(value):
    """
    Convert value to string.

    Convert Python "False" and "True" to lowercase.
    Convert Python "None" to "null".

    :param value: in any format.
    :return: str.
    """
    if type(value) == bool:
        return "true" if value else "false"
    if value is None:
        return "null"
    return str(value)


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
            flag = "+"
            value = dict2[key]
            value = prepare_value_for_comparisons(value)
            comparisons.add_item(flag, key, value)
        elif key not in dict2:  # key only in dict1
            flag = "-"
            value = dict1[key]
            value = prepare_value_for_comparisons(value)
            comparisons.add_item(flag, key, value)
        else:
            value1 = dict1[key]
            value2 = dict2[key]
            if value1 == value2:
                flag = " "
                value = prepare_value_for_comparisons(value1)
                comparisons.add_item(flag, key, value)
            elif type(value1) == dict and type(value2) == dict:
                flag = " "
                sub_comparisons = get_comparison_for_two_dicts(value1, value2)
                comparisons.add_item(flag, key, sub_comparisons)
            else:
                flag = "-"
                value1 = value = prepare_value_for_comparisons(value1)
                comparisons.add_item(flag, key, value1)
                flag = "+"
                value2 = value = prepare_value_for_comparisons(value2)
                comparisons.add_item(flag, key, value2)
    return comparisons


def generate_comparison_output_string(comparisons, level=0) -> str:
    """
    Generate json like string from Comparisons list.

    :param comparisons: Comparisons class.
    :return: str.
    """
    result_string = "{"
    indent = "    " * level
    for comparison in comparisons:
        result_string += "\n"
        flag, key, value = comparison
        if type(value) == Comparisons:
            result_string += f"{indent}  {flag} {key}: "
            result_string += generate_comparison_output_string(value, level + 1)
        else:
            value = convert_value_to_string(value)
            result_string += f"{indent}  {flag} {key}: {value}"
    result_string += f"\n{indent}}}"
    return result_string
