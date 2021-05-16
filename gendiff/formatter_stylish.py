from typing import Any

from gendiff.utilities import unpack_item

FLAGS = {
    "new": "+",
    "removed": "-",
    "updated_new": "+",
    "updated_old": "-",
    "same": " ",
}


def generate_comparison_output_string(
        comparisons: list[dict[str, Any]],
        level: int = 0
) -> str:
    """
    Generate json like string from comparison list.

    :param level: level of nesting, 0 is top, int;
    :param comparisons: comparisons, list[dict[str, Any]].
    :return: str.
    """
    result_string = "{"
    indent = "    " * level
    for comparison in comparisons:
        result_string += "\n"
        key, item_type, node_type, value = unpack_item(comparison)
        flag = FLAGS[item_type]
        if node_type == "branch":
            result_string += f"{indent}  {flag} {key}: "
            result_string += generate_comparison_output_string(value, level + 1)
        else:
            value = convert_value_to_string(value)
            result_string += f"{indent}  {flag} {key}: {value}"
    result_string += f"\n{indent}}}"
    return result_string


def convert_value_to_string(value) -> str:
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
