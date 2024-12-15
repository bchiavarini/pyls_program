import copy
import pytest
from pyls import list_content,PathNotFound

MOCK_STRUCTURE = {
  "name": "interpreter",
  "size": 4096,
  "time_modified": 1699957865,
  "permissions": "-rw-r--r--",
  "contents": [
    {
      "name": ".gitignore",
      "size": 8911,
      "time_modified": 1699941437,
      "permissions": "drwxr-xr-x"
    },
    {
      "name": "LICENSE",
      "size": 1071,
      "time_modified": 1699950073,
      "permissions": "drwxr-xr-x"
    },
    {
      "name": "README.md",
      "size": 83,
      "time_modified": 1699941437,
      "permissions": "drwxr-xr-x"
    }]
}

def test_list_content():
    result = list_content(MOCK_STRUCTURE)
    assert result == ["LICENSE", "README.md"]

def test_include_hidden():
    result = list_content(MOCK_STRUCTURE, include_hidden=True)
    assert result == [".gitignore", "LICENSE", "README.md"]

def test_long_list():
    result = list_content(MOCK_STRUCTURE, long_listing=True)
    assert result == ["drwxr-xr-x   1071 Nov 14 09:21 LICENSE", "drwxr-xr-x     83 Nov 14 06:57 README.md"]

def test_time_sort():
    # make sure of the order of the epoch time
    result = list_content(MOCK_STRUCTURE, time_sort=True)
    assert result == ["README.md","LICENSE"]

def test_filtering():
    structure = copy.deepcopy(MOCK_STRUCTURE)
    dir_element= {
      "name": "ast",
      "size": 4096,
      "time_modified": 1699957739,
      "permissions": "-rw-r--r--",
      "contents": [
        {
          "name": "go.mod",
          "size": 225,
          "time_modified": 1699957780,
          "permissions": "-rw-r--r--"
        }]
    }
    structure["contents"].append(dir_element)
    # test filtering the files
    result_files = list_content(structure, filter="file")
    assert result_files == ["LICENSE", "README.md"]
    # test filtering the directories
    result_dirs = list_content(structure, filter="dir")
    assert result_dirs == ["ast"]

def test_retrieving_path():
    structure = copy.deepcopy(MOCK_STRUCTURE)
    dir_element = {
        "name": "ast",
        "size": 4096,
        "time_modified": 1699957739,
        "permissions": "-rw-r--r--",
        "contents": [
            {
                "name": "go.mod",
                "size": 225,
                "time_modified": 1699957780,
                "permissions": "-rw-r--r--"
            }]
    }
    structure["contents"].append(dir_element)
    # test path relative to the main folder
    result_main_folder_relative = list_content(structure, path=".")
    assert result_main_folder_relative == ["LICENSE", "README.md","ast"]
    # test path relative to the main folder using different prefix
    result_main_folder_relative2 = list_content(structure, path="./")
    assert result_main_folder_relative2 == ["LICENSE", "README.md", "ast"]
    # test a directory path
    result_directory = list_content(structure, path="ast")
    assert result_directory == ["go.mod"]
    # test a file path
    result_file = list_content(structure, path="LICENSE")
    assert result_file == ["LICENSE"]
    # test a relative path of a file
    result_relative_file = list_content(structure, path="./LICENSE")
    assert result_relative_file == ["./LICENSE"]
    # test a file in a directory path
    result_file_in_dir = list_content(structure, path="ast/go.mod")
    assert result_file_in_dir == ["ast/go.mod"]
    # test a relative path of a file in a directory path
    result_file_in_dir_rel = list_content(structure, path="./ast/go.mod")
    assert result_file_in_dir_rel == ["./ast/go.mod"]
    # test a not existing directory
    with pytest.raises(PathNotFound):
        list_content(structure, path="./test")
    # test a not existing file
    with pytest.raises(PathNotFound):
        list_content(structure, path="./ast/test")

def test_human_readable_size():
    result = list_content(MOCK_STRUCTURE, long_listing=True,human_readable=True)
    assert result == ["drwxr-xr-x   1.0K Nov 14 09:21 LICENSE", "drwxr-xr-x     83 Nov 14 06:57 README.md"]



