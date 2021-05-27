from typing import Dict, List, Any


def get_comparisons(  # noqa: C901
        dict1: Dict,
        dict2: Dict
) -> List[Dict[str, Any]]:
    """
    Compare two dictionaries and write all differences in comparison list.

    :param dict1: first dict.
    :param dict2: second dict.
    :return: comparisons, List[Dict[str, Any]].
    """

    def _add_item(_value, item_type):
        item = dict(key=key, item_type=item_type, value=_value)
        comparisons.append(item)

    keys1 = dict1.keys()
    keys2 = dict2.keys()
    all_keys = keys1 | keys2
    comparisons: List[Dict[str, Any]] = []
    for key in sorted(all_keys):
        value1 = dict1.get(key)
        value2 = dict2.get(key)
        if key not in dict1:  # key only in dict2
            _add_item(value2, item_type="new")
        elif key not in dict2:  # key only in dict1
            _add_item(value1, item_type="removed")
        elif value1 == value2:
            _add_item(value1, item_type="same")
        elif isinstance(value1, dict) and isinstance(value2, dict):
            sub_comparisons = get_comparisons(value1, value2)
            _add_item(sub_comparisons, item_type="updated_branch")
        else:
            _add_item(value1, item_type="updated_old")
            _add_item(value2, item_type="updated_new")
    return comparisons
