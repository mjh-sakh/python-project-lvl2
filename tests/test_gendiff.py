import os

import pytest

import gendiff.formatters.formatter_stylish
import gendiff.utilities
from gendiff import generate_diff
from gendiff import parsing

TEST_FOLDER = "tests"
FIXTURES_FOLDER = "fixtures"


class TestClassBlackBoxTests:
    @pytest.mark.parametrize("file1, file2", [
        ("file_flat_1.json", "file_flat_2.json"),
    ])
    def test_generate_diff_return_type_is_string(self, file1, file2):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        assert isinstance(generate_diff(file1, file2), str)

    @pytest.mark.parametrize("file1, file2, expected_result", [
        ("empty.json", "simple.json", "{\n  + test: 1\n}"),
        ("simple.json", "empty.json", "{\n  - test: 1\n}"),
        ("simple.json", "simple.json", "{\n    test: 1\n}"),
        ("file_flat_1.json", "file_flat_2.json",
         "{\n  - follow: false\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: true\n}"),
        ("file_flat_1.yml", "file_flat_2.yaml",
         "{\n  - follow: false\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: true\n}")
    ])
    def test_generate_diff(self, file1, file2, expected_result):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        assert generate_diff(file1, file2) == expected_result

    @pytest.mark.parametrize("file1, file2, file_with_expected_result", [
        ("file_nested_1.json", "file_nested_2.json", "output_nested_stylish.txt"),
        ("file_nested_1.yml", "file_nested_2.yaml", "output_nested_stylish.txt")
    ])
    def test_generate_diff_with_recursion(self, file1, file2, file_with_expected_result):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        file_with_expected_result = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file_with_expected_result)
        with open(file_with_expected_result, 'r') as file:
            expected_result = file.read()
        assert generate_diff(file1, file2) == expected_result

    @pytest.mark.parametrize("file1, file2", [
        ("file_flat_1.json", "file_flat_2.json"),
    ])
    def test_generate_diff_with_none_formatter(self, file1, file2):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        assert isinstance(generate_diff(file1, file2, formatter=None), str)

    @pytest.mark.parametrize("file1, file2, file_with_expected_result", [
        ("file_nested_1.json", "file_nested_2.json", "output_nested_plain.txt"),
        ("file_nested_1.yml", "file_nested_2.yaml", "output_nested_plain.txt")
    ])
    def test_generate_diff_with_plain_formatter(self, file1, file2, file_with_expected_result):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        file_with_expected_result = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file_with_expected_result)
        with open(file_with_expected_result, 'r') as file:
            expected_result = file.read()
        assert generate_diff(file1, file2, formatter='plain') == expected_result

    @pytest.mark.parametrize("file1, file2, file_with_expected_result", [
        ("file_nested_1.json", "file_nested_2.yaml", "output_nested_json.txt")
    ])
    def test_generate_diff_with_json_formatter(self, file1, file2, file_with_expected_result):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        file_with_expected_result = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file_with_expected_result)
        with open(file_with_expected_result, 'r') as file:
            expected_result = file.read()
        assert generate_diff(file1, file2, formatter='json') == expected_result


class TestClassWhiteBoxTests:
    @pytest.mark.parametrize("file_path, expected_result", [
        ("empty.json", {}),
        ("simple.json", {"test": 1}),
    ])
    def test_read_json_from_path_to_dict(self, file_path, expected_result):
        file_path = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file_path)
        assert parsing.read_json_to_dict(file_path) == expected_result

    def test_formatter_proper_bool_representation(self):
        assert gendiff.formatters.formatter_stylish.convert_value_to_string(True) == "true"
        assert gendiff.formatters.formatter_stylish.convert_value_to_string(False) == "false"

    @pytest.mark.parametrize("file_path, expected_result", [
        ("test.json", parsing.read_json_to_dict),
        ("test.yml", parsing.read_yaml_to_dict),
        ("test.yaml", parsing.read_yaml_to_dict)
    ])
    def test_get_proper_reader_for_file(self, file_path, expected_result):
        assert parsing.get_proper_read_to_dict(file_path) is expected_result
