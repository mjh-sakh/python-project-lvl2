import pytest
from gendiff import generate_diff


@pytest.mark.parametrize("file1, file2", [
    ("file1.json", "file2.json"),
])
def test_return_type_is_string(file1, file2):
    assert type(generate_diff.generate_diff(file1, file2)) == str


# def test_output_string_format():
#     empty_json = "empty.json"
#     simple_json = "simple.json"
#     resulting_string = generate_diff(empty_json, simple_json)
#
#
# def test_same_file():
#     file1 = file2 = "file1.json"
#     file_content = json.load(file1)
#     assert generate_diff

@pytest.mark.parametrize("file_path, expected_result", [
    ("tests/empty.json", {}),
    ("tests/simple.json", {"test": 1}),
])
def test_read_json_from_path_to_dict(file_path, expected_result):
    assert generate_diff.read_json_from_path_to_dict(file_path) == expected_result


@pytest.mark.parametrize("file1, file2, expected_result", [
    ("tests/empty.json", "tests/simple.json", [("+", "test", "1")]),
    ("tests/simple.json", "tests/empty.json", [("-", "test", "1")]),
    ("tests/simple.json", "tests/simple.json", [(" ", "test", "1")]),
])
def test_comparison_(file1, file2, expected_result):
    dict1 = generate_diff.read_json_from_path_to_dict(file1)
    dict2 = generate_diff.read_json_from_path_to_dict(file2)
    assert generate_diff.get_comparison_for_two_dicts(dict1, dict2) == expected_result


def test_Comparisons_class_equals():
    comp1 = generate_diff.Comparisons()
    comp1.add_item(" ", "key", "value")
    assert comp1 == comp1
    assert comp1 == [(" ", "key", "value")]
    assert not comp1 == []
