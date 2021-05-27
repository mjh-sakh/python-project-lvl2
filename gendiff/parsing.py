import json
import os
from typing import Callable

import yaml


def get_proper_read_to_dict(file_path: str) -> Callable:
    """
    Get proper function to read specific file based on file extension.

    :param file_path: str.
    :return: json or yaml read to dict function.
    """
    extension = os.path.splitext(file_path)[-1]
    if extension == ".json":
        return json.loads
    elif extension in (".yml", ".yaml"):
        return yaml.safe_load
    raise NotImplementedError(f"Unsupported file type {extension}")
