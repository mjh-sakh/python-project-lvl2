from typing import Callable

from gendiff.formatters import formatter_stylish, formatter_plain, formatter_json  # noqa: E501


def get_formatter(formatter: str) -> Callable:
    """
    Get proper formatter function to generate string.

    :param formatter: stylish, plain or json, str.
    :return: formatter function.
    """
    if formatter == 'stylish':
        return formatter_stylish.generate_comparison_output_string
    elif formatter == "plain":
        return formatter_plain.generate_comparison_output_string
    elif formatter == "json":
        return formatter_json.generate_comparison_output_string
    else:
        raise NotImplementedError('Formatter "{formatter}" is not implemented. Choose "stylish"')  # noqa: E501
