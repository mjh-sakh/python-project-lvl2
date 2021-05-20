import numbers
from typing import Any, List, Dict

from gendiff.utilities import unpack_item


def generate_comparison_output_string(
        comparisons: List[Dict[str, Any]],
) -> str:
    long_string = generate_comparison_output_long_string(comparisons)
    if long_string:
        short_string = long_string[:-1]  # removing last \n
        return short_string
    return long_string


def generate_comparison_output_long_string(  # noqa: C901
        comparisons: List[Dict[str, Any]],
        parent_key: str = ""
) -> str:
    """
    Generate plain formatted string from comparison list.

    :param parent_key: name of parent key,  str.
    :param comparisons: comparisons, List[Dict[str, Any]].
    :return: str.
    """
    result_string = ""
    for comparison in comparisons:
        key, item_type, node_type, value = unpack_item(comparison)
        key_full_path = f"{parent_key}.{key}" if parent_key else key
        if node_type == "branch" and item_type == "same":
            result_string += generate_comparison_output_long_string(value, parent_key=key_full_path)  # noqa: E501
        else:
            value = convert_value_to_string(value)
            if item_type == "updated_new":
                result_string += f"{value}\n"
            elif item_type == "same":
                pass
            else:
                result_string += f"Property '{key_full_path}' was "
                if item_type == "new":
                    result_string += f"added with value: {value}\n"
                elif item_type == "removed":
                    result_string += "removed\n"
                elif item_type == "updated_old":
                    result_string += f"updated. From {value} to "
    return result_string


def convert_value_to_string(value: Any) -> str:
    """
    Convert value to string.

    Convert Python "False" and "True" to lowercase.
    Convert Python "None" to "null".
    Adds '' around String.
    Convert other types to "[complex value]".

    :param value: in any format.
    :return: str.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, str):
        return f"'{value}'"
    if isinstance(value, numbers.Number):
        return str(value)
    return "[complex value]"
