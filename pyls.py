import argparse
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

CONFIG_FILEPATH = "structure.json"


class JsonDecoderException(Exception):
    """Exception raised when the config Json object cannot be decoded."""

class ArgsValidationException(Exception):
    """Exception raised when argument does not pass validation."""


def convert_time(epoch_time: int) -> str:
    # convert epoch time to datetime relative to the user time zone
    dt_object = datetime.fromtimestamp(epoch_time)
    formatted_time = dt_object.strftime('%b %d %H:%M')
    return formatted_time


def list_content(structure: Dict[str, Any],
                 include_hidden: bool = False,
                 long_listing: bool = False,
                 time_sort:bool = False,
                 filter:Optional[str]=None) -> List[str]:
    content: List[str] = []

    if time_sort:
        # sort the contents in structure by time
        sorted_content=sorted(structure["contents"], key=lambda x: x["time_modified"])
        content_to_parse = sorted_content
    else:
        content_to_parse = structure["contents"]

    for el in content_to_parse:
        if el["name"].startswith(".") and not include_hidden:
            # ignore the hidden files
            continue

        if filter:
            if filter == "file" and "contents" in el:
                # if the element has contents it is a directory: ignore
                continue
            if filter == "dir" and not "contents" in el:
                # if the element does not have contents it is a file: ignore
                continue

        if long_listing:
            # convert epoch time to human-readable time
            modified_time = convert_time(el["time_modified"])
            # format the output to align the elements in columns
            content_el = f"{el['permissions']:<10} {el['size']:>6} {modified_time:<10} {el["name"]}"
            content.append(content_el)
        else:
            content.append(el["name"])
    return content


def main():
    parser = argparse.ArgumentParser(prog="ls",
                                     description=f"List the contents of directories described in {CONFIG_FILEPATH}")
    parser.add_argument('-A', dest='include_hidden', action='store_true',
                        help='List all contents including hidden files and directories')
    parser.add_argument('-l', dest='long_listing', action='store_true',
                        help='Use a long listing format')
    parser.add_argument('-r', dest='reverse', action='store_true',
                        help='Reverse order while sorting')
    parser.add_argument('-t', dest='time_sort', action='store_true',
                        help='Sort by modification time (oldest first)')
    parser.add_argument("--filter", dest='filter', type=str,
                        help="Filter the content to list only files or directories. Only 'file' and 'dir' values are accepted.")
    args = parser.parse_args()

    if args.filter and args.filter not in ["file", "dir"]:
        raise ArgsValidationException(f"'{args.filter}' is not a valid filter criteria. Available filters are 'dir' and 'file'")

    config_file = Path(CONFIG_FILEPATH)
    if not config_file.exists() or not config_file.is_file():
        raise FileNotFoundError("structure.json not found")
    # open the structure file
    try:
        with open(config_file, 'r') as f:
            directories_structure = json.load(f)
    except Exception:
        raise JsonDecoderException("structure.json cannot be read")

    content = list_content(directories_structure,
                           include_hidden=args.include_hidden,
                           long_listing=args.long_listing,
                           time_sort=args.time_sort,
                           filter=args.filter)
    if args.reverse:
        # reverse the content order
        content.reverse()
    if args.long_listing:
        # in case of long listing, print in column
        for el in content:
            print(el)
    else:
        print(" ".join(content))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
