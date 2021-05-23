from typing import Any, List, Dict

from gendiff.utilities import unpack_item

FLAGS = {
    "new": "+",
    "removed": "-",
    "updated_new": "+",
    "updated_old": "-",
    "updated_branch": " ",
    "same": " ",
}

INDENT = "    "


def generate_comparison_output_string(
        comparisons: List[Dict[str, Any]],
        level: int = 0
) -> str:
    """
    Generate json like string from comparison list.

    :param level: level of nesting, 0 is top, int;
    :param comparisons: comparisons, List[Dict[str, Any]].
    :return: str.
    """
    result_string = "{"
    indent = INDENT * level
    for comparison in comparisons:
        result_string += "\n"
        key, item_type, value = unpack_item(comparison)
        flag = FLAGS[item_type]
        if item_type == "updated_branch":
            result_string += f"{indent}  {flag} {key}: "
            result_string += generate_comparison_output_string(value, level + 1)
        else:
            value = convert_value_to_string(value, indent=indent + INDENT)
            result_string += f"{indent}  {flag} {key}: {value}"
    result_string += f"\n{indent}}}"
    return result_string


def convert_value_to_string(value: Any, indent: str = INDENT) -> str:
    """
    Convert value to string.

    Convert Python "False" and "True" to lowercase.
    Convert Python "None" to "null".

    :param indent: indent via spaces, str.
    :param value: in any format.
    :return: str.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, dict):
        string: str = "{\n"
        for key, _value in value.items():
            string += f"{INDENT}{indent}{key}: "
            string += convert_value_to_string(_value, indent=indent + INDENT)
            string += "\n"
        string += f"{indent}}}"
        return string
    return str(value)
