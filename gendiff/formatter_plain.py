from gendiff.data_type import Comparisons
from gendiff.formatter_stylish import convert_value_to_string


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