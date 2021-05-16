from typing import Any


def unpack_item(item: dict[str, Any]) -> tuple[Any, str, str, Any]:
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
