import argparse
from pathlib import Path
from typing import Any, Dict, List
import json

CONFIG_FILEPATH = "structure.json"

class JsonDecoderException(Exception):
    """Exception raised when the config Json object cannot be decoded."""


def list_content(structure:Dict[str, Any]) -> List[str]:
    content:List[str] = []
    for el in structure["contents"]:
        if not el["name"].startswith("."):
            # ignore the hidden files
            content.append(el["name"])
    return content

def format_output(content:List[str]) -> str:
    return " ".join(content)


def main():
    parser = argparse.ArgumentParser(prog="ls",description="List the contents of directories")
    args = parser.parse_args()
    config_file= Path(CONFIG_FILEPATH)
    if not config_file.exists() or not config_file.is_file():
        raise FileNotFoundError("structure.json not found")
    # open the structure file
    try:
        with open(config_file, 'r') as f:
            directories_structure = json.load(f)
    except Exception:
        raise JsonDecoderException("structure.json cannot be read")

    content = list_content(directories_structure)
    formatted_output = format_output(content)
    print(formatted_output)



if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")