from gendiff.data_type import Comparisons


def generate_comparison_output_string(comparisons, level: int = 0) -> str:
    """
    Generate json like string from Comparisons list.

    :param level: level of nesting, 0 is top, int;
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
