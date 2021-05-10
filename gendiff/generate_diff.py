from gendiff.parsing import read_json_from_path_to_dict


def generate_diff(file1: str, file2: str) -> str:
    """
    Generate comparison between two files.

    :param file1: path to file 1.
    :param file2: path to file 2.
    :return: comparison string in json-like format.
    """
    dict1 = read_json_from_path_to_dict(file1)
    dict2 = read_json_from_path_to_dict(file2)
    comparisons = get_comparison_for_two_dicts(dict1, dict2)
    comparisons_string = generate_comparison_output_string(comparisons)
    return comparisons_string


class Comparisons(list):
    """
    Container to store per-value comparisons based on list.
    Provides two methods on top of list type:
      add_time: adds tuple to the list (flag, key, value)
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
        value = self.convert_value_to_string(value)
        self.append((flag, key, value))

    def convert_value_to_string(self, value):
        """
        Convert value to string.

        Convert Python "False" and "True" to lowercase.

        :param value: in any format.
        :return: str.
        """
        if type(value) == bool:
            return "true" if value else "false"
        return str(value)

    # def __getitem__(self, item):
    #     return dict(zip(["flag", "key", "value"], super().__getitem__(item)))


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
            comparisons.add_item(flag, key, value)
        elif key not in dict2:  # key only in dict1
            flag = "-"
            value = dict1[key]
            comparisons.add_item(flag, key, value)
        else:
            value1 = dict1[key]
            value2 = dict2[key]
            if value1 == value2:
                flag = " "
                comparisons.add_item(flag, key, value1)
            else:
                flag = "-"
                comparisons.add_item(flag, key, value1)
                flag = "+"
                comparisons.add_item(flag, key, value2)
    return comparisons


def generate_comparison_output_string(comparisons) -> str:
    """
    Generate json like string from Comparisons list.

    :param comparisons: Comparisons class.
    :return: str.
    """
    result_string = "{"
    flag_to_add_trailing_comma = False
    for comparison in comparisons:
        result_string += ",\n" if flag_to_add_trailing_comma else "\n"
        flag, key, value = comparison
        result_string += f"  {flag} {key}: {value}"
    result_string += "\n}"
    return result_string
