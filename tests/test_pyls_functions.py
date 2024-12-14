from pyls import list_content, format_output

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
      "time_modified": 1699941437,
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


def test_format_output():
    content = ["file1.txt", "file2.txt"]
    result = format_output(content)
    assert result == "file1.txt file2.txt"