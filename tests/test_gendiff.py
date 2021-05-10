import pytest
import os
from gendiff import generate_diff

TEST_FOLDER = "tests"
FIXTURES_FOLDER = "fixtures"


@pytest.mark.parametrize("file1, file2", [
    ("file1.json", "file2.json"),
])
def test_generate_diff_return_type_is_string(file1, file2):
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
def test_generate_diff(file1, file2, expected_result):
    file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
    file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
    assert generate_diff.generate_diff(file1, file2) == expected_result


@pytest.mark.parametrize("file_path, expected_result", [
    ("empty.json", {}),
    ("simple.json", {"test": 1}),
])
def test_read_json_from_path_to_dict(file_path, expected_result):
    file_path = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file_path)
    assert generate_diff.read_json_from_path_to_dict(file_path) == expected_result


@pytest.mark.parametrize("file1, file2, expected_result", [
    ("empty.json", "simple.json", [("+", "test", "1")]),
    ("simple.json", "empty.json", [("-", "test", "1")]),
    ("simple.json", "simple.json", [(" ", "test", "1")]),
])
def test_get_comparison_for_two_dicts(file1, file2, expected_result):
    file1 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file1)
    file2 = os.path.join(TEST_FOLDER, FIXTURES_FOLDER, file2)
    dict1 = generate_diff.read_json_from_path_to_dict(file1)
    dict2 = generate_diff.read_json_from_path_to_dict(file2)
    assert generate_diff.get_comparison_for_two_dicts(dict1, dict2) == expected_result


@pytest.fixture
def example_comparisons():
    comparisons = generate_diff.Comparisons()
    comparisons.add_item(" ", "test_str", "value")
    comparisons.add_item("+", "test_int", 1)
    comparisons.add_item("+", "test_float", 3.14)
    comparisons.add_item("+", "test_bool", True)
    comparisons.add_item("+", "test_bool", False)
    return comparisons


def test_Comparisons_class_content_to_be_all_strings(example_comparisons):
    for items in example_comparisons:
        assert all(map(lambda x: type(x) == str, items))


def test_Comparisons_class_proper_bool_represenation():
    comparisons = generate_diff.Comparisons()
    comparisons.add_item(" ", "True", True)
    comparisons.add_item(" ", "False", False)
    assert comparisons[0][2] == "true"
    assert comparisons[1][2] == "false"


def test_Comparisons_class_equals():
    comparisons = generate_diff.Comparisons()
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
def test_generate_comparison_output_string_format(comparisons_item, expected_result):
    comparisons = generate_diff.Comparisons()
    comparisons.add_item(*comparisons_item)
    assert generate_diff.generate_comparison_output_string(comparisons) == expected_result
