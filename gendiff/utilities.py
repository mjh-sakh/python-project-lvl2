from typing import Any, Dict, Tuple


def unpack_item(item: Dict[str, Any]) -> Tuple[Any, str, Any]:
    """
    Unpack comparison item.

    :param item: comparison, dict[str, Any]
    :return: key, item_type, value
    """
    key = item["key"]
    item_type = item["item_type"]
    value = item["value"]
    return key, item_type, value


def read_text_from_file(file_path: str) -> str:
    """
    Open file, read it and return text.
    """
    with open(file_path, 'r') as file:
        text = file.read()
    return text
