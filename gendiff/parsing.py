import json
import os
from typing import Dict, Callable

import yaml


def get_proper_read_to_dict_for_file(file_path: str) -> Callable:
    """
    Get proper function to read specific file based on file extension.

    :param file_path: str.
    :return: json or yaml read to dict function.
    """
    extension = os.path.splitext(file_path)[-1]
    if extension == ".json":
        return read_json_from_path_to_dict
    elif extension in (".yml", ".yaml"):
        return read_yaml_from_path_to_dict
    raise NotImplementedError(f"Unsupported file type {extension}")


def read_json_from_path_to_dict(file_path: str) -> Dict:
    """
    Read json file to Python dictionary.

    :param file_path: str.
    :return: dict.
    """
    with open(file_path, 'r') as file:
        python_dict = json.load(file)
    return python_dict


def read_yaml_from_path_to_dict(file_path: str) -> Dict:
    """
    Read yaml file to Python dictionary.

    :param file_path: str.
    :return: dict.
    """
    with open(file_path, 'r') as file:
        python_dict = yaml.safe_load(file)
    return python_dict
