import pytest
import os

import gendiff.data_type
import gendiff.formatter_stylish
from gendiff import generate_diff
from gendiff import parsing

TEST_FOLDER = "tests"
FIXTURES_FOLDER = "fixtures"


class TestClassBlackBoxTests():
    @pytest.mark.parametrize("file1, file2", [
        ("file1.json", "file2.json"),
    ])
    def test_generate_diff_return_type_is_string(self, file1, file2):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        assert type(generate_diff.generate_diff(file1, file2)) == str

    @pytest.mark.parametrize("file1, file2, expected_result", [
        ("empty.json", "simple.json", "{\n  + test: 1\n}"),
        ("simple.json", "empty.json", "{\n  - test: 1\n}"),
        ("simple.json", "simple.json", "{\n    test: 1\n}"),
        ("file1.json", "file2.json",
         "{\n  - follow: false\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: true\n}"),
        ("file1.yml", "file2.yaml",
         "{\n  - follow: false\n    host: hexlet.io\n  - proxy: 123.234.53.22\n  - timeout: 50\n  + timeout: 20\n  + verbose: true\n}")
    ])
    def test_generate_diff(self, file1, file2, expected_result):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        assert generate_diff.generate_diff(file1, file2) == expected_result

    @pytest.mark.parametrize("file1, file2, file_with_expected_result", [
        ("file3.json", "file4.json", "output_stylish_file3_file4.txt"),
        ("file5.yml", "file6.yaml", "output_stylish_file5_file6.txt")
    ])
    def test_generate_diff_with_recursion(self, file1, file2, file_with_expected_result):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        file_with_expected_result = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file_with_expected_result)
        with open(file_with_expected_result, 'r') as file:
            expected_result = file.read()
        assert generate_diff.generate_diff(file1, file2) == expected_result

    @pytest.mark.parametrize("file1, file2", [
        ("file1.json", "file2.json"),
    ])
    def test_generate_diff_with_none_formatter(self, file1, file2):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        assert type(generate_diff.generate_diff(file1, file2, formatter=None)) == str

    @pytest.mark.parametrize("file1, file2, file_with_expected_result", [
        ("file3.json", "file4.json", "output_plain_file3_file4.txt"),
        ("file5.yml", "file6.yaml", "output_plain_file5_file6.txt")
    ])
    def test_generate_diff_with_plain_formatter(self, file1, file2, file_with_expected_result):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        file_with_expected_result = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file_with_expected_result)
        with open(file_with_expected_result, 'r') as file:
            expected_result = file.read()
        assert generate_diff.generate_diff(file1, file2, formatter='plain') == expected_result

class TestClassWhiteBoxTests():
    @pytest.mark.parametrize("file_path, expected_result", [
        ("empty.json", {}),
        ("simple.json", {"test": 1}),
    ])
    def test_read_json_from_path_to_dict(self, file_path, expected_result):
        file_path = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file_path)
        assert parsing.read_json_from_path_to_dict(file_path) == expected_result

    @pytest.mark.parametrize("file1, file2, expected_result", [
        ("empty.json", "simple.json", [("+", "test", 1)]),
        ("simple.json", "empty.json", [("-", "test", 1)]),
        ("simple.json", "simple.json", [(" ", "test", 1)]),
    ])
    def test_get_comparison_for_two_dicts(self, file1, file2, expected_result):
        file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
        file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
        dict1 = parsing.read_json_from_path_to_dict(file1)
        dict2 = parsing.read_json_from_path_to_dict(file2)
        assert generate_diff.get_comparison_for_two_dicts(dict1, dict2) == expected_result

    @pytest.fixture
    def example_comparisons(self):
        comparisons = gendiff.data_type.Comparisons()
        comparisons.add_item(" ", "test_str", "value")
        comparisons.add_item("+", "test_int", 1)
        comparisons.add_item("+", "test_float", 3.14)
        comparisons.add_item("+", "test_bool", True)
        comparisons.add_item("+", "test_bool", False)
        return comparisons

    def test_Comparisons_class_proper_bool_represenation(self):
        assert gendiff.formatter_stylish.convert_value_to_string(True) == "true"
        assert gendiff.formatter_stylish.convert_value_to_string(False) == "false"

    def test_Comparisons_class_equals(self):
        comparisons = gendiff.data_type.Comparisons()
        item = (" ", "key", "value")
        comparisons.add_item(*item)
        assert comparisons == comparisons
        assert comparisons == [item]
        assert not comparisons == []

    @pytest.mark.parametrize("comparisons_item, expected_result", [
        (("+", "test", "1"), "{\n  + test: 1\n}"),
        (("-", "test", "1"), "{\n  - test: 1\n}"),
        ((" ", "test", "1"), "{\n    test: 1\n}"),
    ])
    def test_generate_comparison_output_string_format(self, comparisons_item, expected_result):
        comparisons = gendiff.data_type.Comparisons()
        comparisons.add_item(*comparisons_item)
        assert gendiff.formatter_stylish.generate_comparison_output_string(comparisons) == expected_result

    @pytest.mark.parametrize("file_path, expected_result", [
        ("test.json", parsing.read_json_from_path_to_dict),
        ("test.yml", parsing.read_yaml_from_path_to_dict),
        ("test.yaml", parsing.read_yaml_from_path_to_dict)
    ])
    def test_get_proper_reader_for_file(self, file_path, expected_result):
        assert parsing.get_proper_read_to_dict_for_file(file_path) is expected_result
