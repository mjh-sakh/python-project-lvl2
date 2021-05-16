from typing import Any, Dict, Tuple


def unpack_item(item: Dict[str, Any]) -> Tuple[Any, str, str, Any]:
    """
    Unpack comparison item.

    :param item: comparison, dict[str, Any]
    :return: key, item_type, node_type, value
    """
    key = item["key"]
    item_type = item["item_type"]
    node_type = item["node_type"]
    value = item["value"]
    return key, item_type, node_type, value