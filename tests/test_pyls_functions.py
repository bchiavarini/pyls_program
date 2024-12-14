from pyls import list_content, format_output


def test_list_content():
    structure = {
        "contents": [
            {"name": "file1.txt"},
            {"name": ".hiddenfile"},
            {"name": "file2.txt"}
        ]
    }
    result = list_content(structure)
    assert result == ["file1.txt", "file2.txt"]


def test_format_output():
    content = ["file1.txt", "file2.txt"]
    result = format_output(content)
    assert result == "file1.txt file2.txt"