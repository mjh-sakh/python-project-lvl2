import os

import pytest

import gendiff.formatters.formatter_stylish
from gendiff import generate_diff
from gendiff.utilities import read_text

TEST_FOLDER = "tests"
FIXTURES_FOLDER = "fixtures"


def locate(file_name):
    file_path = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file_name)
    return file_path


class TestClassBlackBoxTests:
    @pytest.mark.parametrize("file1, file2", [
        ("file_flat_1.json", "file_flat_2.json"),
    ])
    def test_generate_diff_return_type_is_string(self, file1, file2):
        assert isinstance(generate_diff(locate(file1), locate(file2)), str)

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
        assert generate_diff(locate(file1), locate(file2)) == expected_result

    @pytest.mark.parametrize("file1, file2, file_with_expected_result", [
        ("file_nested_1.json", "file_nested_2.json", "output_nested_stylish.txt"),
        ("file_nested_1.yml", "file_nested_2.yaml", "output_nested_stylish.txt")
    ])
    def test_generate_diff_with_recursion(self, file1, file2, file_with_expected_result):
        expected_result = read_text(locate(file_with_expected_result))
        assert generate_diff(locate(file1), locate(file2)) == expected_result

    @pytest.mark.parametrize("file1, file2", [
        ("file_flat_1.json", "file_flat_2.json"),
    ])
    def test_generate_diff_with_none_formatter(self, file1, file2):
        assert isinstance(generate_diff(locate(file1), locate(file2), formatter=None), str)

    @pytest.mark.parametrize("file1, file2, file_with_expected_result", [
        ("file_nested_1.json", "file_nested_2.json", "output_nested_plain.txt"),
        ("file_nested_1.yml", "file_nested_2.yaml", "output_nested_plain.txt")
    ])
    def test_generate_diff_with_plain_formatter(self, file1, file2, file_with_expected_result):
        expected_result = read_text(locate(file_with_expected_result))
        assert generate_diff(locate(file1), locate(file2), formatter='plain') == expected_result

    @pytest.mark.parametrize("file1, file2, file_with_expected_result", [
        ("file_nested_1.json", "file_nested_2.yaml", "output_nested_json.txt")
    ])
    def test_generate_diff_with_json_formatter(self, file1, file2, file_with_expected_result):
        expected_result = read_text(locate(file_with_expected_result))
        assert generate_diff(locate(file1), locate(file2), formatter='json') == expected_result


class TestClassWhiteBoxTests:
    @pytest.mark.parametrize("file, expected_result", [
        ("simple.json", '{\n  "test": 1\n}')
    ])
    def test_read_text(self, file, expected_result):
        assert read_text(locate(file)) == expected_result

    def test_formatter_proper_bool_representation(self):
        assert gendiff.formatters.formatter_stylish.convert_value_to_string(True) == "true"
        assert gendiff.formatters.formatter_stylish.convert_value_to_string(False) == "false"
