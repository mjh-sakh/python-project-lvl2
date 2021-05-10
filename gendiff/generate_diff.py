import json


def generate_diff(file1: str, file2: str) -> str:
    return "Yep, it's string - going with TDD, bro :)"


def read_json_from_path_to_dict(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        json_dict = json.load(file)
    return json_dict


def get_comparison_for_two_dicts(dict1: dict, dict2: dict):
    keys1 = dict1.keys()
    keys2 = dict2.keys()
    all_keys = keys1 | keys2
    comparisons = Comparisons()
    flag = ""
    value = None
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


class Comparisons(object):
    def __init__(self):
        self.comparison_list = []

    def add_item(self, flag, key, value):
        value = self.convert_value(value)
        self.comparison_list.append((flag, key, value))

    def convert_value(self, value):
        if type(value) == bool:
            return "true" if value else "false"
        return str(value)

    def __repr__(self):
        return str(self.comparison_list)

    def __eq__(self, other):
        return self.comparison_list == other
