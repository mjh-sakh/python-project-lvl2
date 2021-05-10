import json


def read_json_from_path_to_dict(file_path: str) -> dict:
    """
    Read json file to Python dictionary.

    :param file_path: str.
    :return: dict.
    """
    with open(file_path, 'r') as file:
        json_dict = json.load(file)
    return json_dict


def read_yaml_from_path_to_dict(file_path: str) -> dict:
    assert False, "Not implemented"
