from pyls import list_content

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