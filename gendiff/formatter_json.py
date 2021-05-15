from gendiff.data_type import Comparisons
import json


def generate_comparison_output_string(comparisons) -> str:
    """
    Generate json string that encodes Comparisons list.

    :param comparisons: Comparisons class.
    :return: str.
    """
    result_dict = generate_comparison_dict(comparisons)
    result_string = json.dumps(result_dict, sort_keys=True, indent=4)
    return result_string


def generate_comparison_dict(comparisons, parent_key=None) -> dict:
    result_dict = dict()
    for line_count, comparison in enumerate(comparisons):
        flag, key, value = comparison
        dict_key = str(line_count) if parent_key is None else f"{parent_key}.{line_count}"  # noqa: E501
        result_dict[dict_key] = [flag, key]
        if type(value) == Comparisons:
            result_dict[dict_key].append(generate_comparison_dict(value, parent_key=dict_key))  # noqa: E501
        else:
            result_dict[dict_key].append(value)
    return result_dict
