from gendiff.data_type import Comparisons, FLAGS
import numbers


def generate_comparison_output_string(comparisons, parent_key: str = "") -> str:
    """
    Generate plain formatted string from Comparisons list.

    :param parent_key: name of parent key,  str.
    :param comparisons: Comparisons class.
    :return: str.
    """
    result_string = ""
    for comparison in comparisons:
        flag, key, value = comparison
        key_full_path = f"{parent_key}.{key}" if parent_key else key
        if type(value) == Comparisons and flag[0] == 'u':
            result_string += generate_comparison_output_string(value, parent_key=key_full_path)
        else:
            value = convert_value_to_string(value)
            if flag == FLAGS["changed_new"]:
                result_string += f"{value}\n"
            elif flag == FLAGS["unchanged"]:
                pass
            else:
                result_string += f"Property '{key_full_path}' was "
                if flag == FLAGS["new"]:
                    result_string += f"added with value: {value}\n"
                elif flag == FLAGS["removed"]:
                    result_string += "removed\n"
                elif flag == FLAGS["changed_old"]:
                    result_string += f"updated. From {value} to "
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
    if type(value) == str:
        return f"'{value}'"
    if isinstance(value, numbers.Number):
        return str(value)
    return "[complex value]"
