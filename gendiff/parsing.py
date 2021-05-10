import json
import os


def get_proper_reader_for_file(file_path: str):
    assert os.path.isfile(file_path), f"{file_path} is not a file."
    file_name = os.path.split(file_path)[-1]
    extension = file_name.split('.')[-1]
    if extension == "json":
        return read_json_from_path_to_dict
    elif extension in ("yml", "yaml"):
        return read_yaml_from_path_to_dict
    assert True, f"Unsupported file type {extension}"


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
