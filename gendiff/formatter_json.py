import json

from gendiff.utilities import unpack_item


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
        key, item_type, node_type, value = unpack_item(comparison)
        dict_key = str(line_count) if parent_key is None else f"{parent_key}.{line_count}"  # noqa: E501
        if node_type == "branch":
            value = generate_comparison_dict(value, parent_key=dict_key)
            result_dict[dict_key] = dict(key=key, item_type="same", node_type="branch", value=value)  # noqa: E501
        else:
            result_dict[dict_key] = comparison
    return result_dict
