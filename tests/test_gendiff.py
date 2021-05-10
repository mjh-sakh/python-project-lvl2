import pytest
from gendiff import generate_diff


@pytest.fixture
def test_json_files_1():
    file1_path = "file1.json"
    file2_path = "file2.json"
    return file1_path, file2_path


def test_return_type_is_string(test_json_files_1):
    file1_path, file2_path = test_json_files_1
    assert type(generate_diff.generate_diff(file1_path, file2_path)) == str
