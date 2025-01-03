import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

CONFIG_FILEPATH = "structure.json"


class JsonDecoderException(Exception):
    """Exception raised when the config Json object cannot be decoded."""


class ArgsValidationException(Exception):
    """Exception raised when argument does not pass validation."""


class PathNotFound(Exception):
    """Exception raised when the selected path cannot be found in the structure"""


class NoContentException(Exception):
    """Exception raised when no content can be found in the structure"""


def convert_time(epoch_time: int) -> str:
    # convert epoch time to datetime relative to the user time zone
    dt_object = datetime.fromtimestamp(epoch_time)
    formatted_time = dt_object.strftime("%b %d %H:%M")
    return formatted_time


def convert_size(size_bytes: int) -> str:
    units = ["B", "K", "M", "G"]
    size = float(size_bytes)
    if size < 1024:
        # if there are only bytes, do not add the unit label
        return str(int(size))
    unit_index = 0
    # keep dividing until the resulting size is <1024
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    # format the result
    if size.is_integer():
        # if it is an integer do no add decimals
        size = int(size)
    else:
        # if it is a float, it is rounded to 2 decimals
        size = round(size, 1)

    return f"{size}{units[unit_index]}"


def get_root(structure: Dict[str, Any], path: str) -> Optional[Dict[str, Any]]:
    root_dir: Optional[Dict[str, Any]] = None
    for el in structure["contents"]:
        if el["name"] == path:
            if "contents" not in el:
                # this is a file. Use the same json structure
                root_dir = {"contents": [el]}
            else:
                root_dir = el
    if not root_dir:
        # it means that the path does not exist
        raise PathNotFound(f"cannot access '{path}': No such file or directory")
    return root_dir


def list_content(
    structure: Dict[str, Any],
    include_hidden: bool = False,
    long_listing: bool = False,
    time_sort: bool = False,
    filter: Optional[str] = None,
    path: Optional[str] = None,
    human_readable: bool = False,
) -> List[str]:
    content: List[str] = []
    # the default root is the root dir specified in the json
    root = structure
    name_prefix = ""
    # ignore relative path to the current directory
    if path and path not in [".", "./"]:
        prefix = ""
        if path.startswith("./"):
            # this path is relative to the main folder. Ignore the relative prefix
            path = path.lstrip("./")
            # add the relative path to prefix that will be used for filenames
            prefix = "./"

        # split the path to get the subdirectories
        path_structure = path.split("/")
        # build the relative prefix that will be used for filenames
        if len(path_structure) > 1:
            prefix += "/".join(path_structure[:-1]) + "/"

        for p in path_structure:
            # choose recursively the given path as root directory
            root = get_root(root, p)

        # add the prefix to the name only if the contents are files
        if "name" not in root:
            # if there are only contents with no name it means that the resulting path is a path of a single file
            name_prefix = prefix

    if time_sort:
        # sort the contents in structure by time
        sorted_content = sorted(root["contents"], key=lambda x: x["time_modified"])
        content_to_parse = sorted_content
    else:
        content_to_parse = root["contents"]

    for el in content_to_parse:
        if el["name"].startswith(".") and not include_hidden:
            # ignore the hidden files
            continue

        if filter:
            if filter == "file" and "contents" in el:
                # if the element has contents it is a directory: ignore
                continue
            if filter == "dir" and "contents" not in el:
                # if the element does not have contents it is a file: ignore
                continue

        if long_listing:
            # convert epoch time to human-readable time
            modified_time = convert_time(el["time_modified"])
            if human_readable:
                # convert the size to a human-readable format
                el["size"] = convert_size(el["size"])
            # format the output to align the elements in columns
            content_el = f"{el['permissions']:<10} {el['size']:>6} {modified_time:<10} {name_prefix}{el['name']}"
            content.append(content_el)
        else:
            content.append(f"{name_prefix}{el['name']}")
    return content


def main():
    parser = argparse.ArgumentParser(
        prog="ls",
        description=f"List the contents of directories described in {CONFIG_FILEPATH}",
        add_help=False,
    )
    parser.add_argument(
        "-A",
        dest="include_hidden",
        action="store_true",
        help="List all contents including hidden files and directories",
    )
    parser.add_argument(
        "-l", dest="long_listing", action="store_true", help="Use a long listing format"
    )
    parser.add_argument(
        "-r", dest="reverse", action="store_true", help="Reverse order while sorting"
    )
    parser.add_argument(
        "-t",
        dest="time_sort",
        action="store_true",
        help="Sort by modification time (oldest first)",
    )
    parser.add_argument(
        "--filter",
        dest="filter",
        type=str,
        help="Filter the content to list only files or directories. Only 'file' and 'dir' values are accepted.",
    )
    parser.add_argument(
        "path",
        type=str,
        nargs="?",
        help=" (Optional) List the contents relative to a specific path. Paths relative to the main directory are also supported",
    )
    parser.add_argument(
        "-h",
        dest="human_readable",
        action="store_true",
        help="With -l, print size like 2K 100M 3G etc.",
    )
    parser.add_argument(
        "--help",
        dest="help",
        action="store_true",
        help="Show this help message and exit",
    )

    args = parser.parse_args()
    if args.help:
        parser.print_help()
        exit(0)

    if args.filter and args.filter not in ["file", "dir"]:
        raise ArgsValidationException(
            f"'{args.filter}' is not a valid filter criteria. Available filters are 'dir' and 'file'"
        )

    config_file = Path(CONFIG_FILEPATH)
    if not config_file.exists() or not config_file.is_file():
        raise FileNotFoundError("structure.json not found")
    # open the structure file
    try:
        with open(config_file) as f:
            directories_structure = json.load(f)
    except Exception:
        raise JsonDecoderException(f"{CONFIG_FILEPATH} cannot be read")

    content = list_content(
        directories_structure,
        include_hidden=args.include_hidden,
        long_listing=args.long_listing,
        time_sort=args.time_sort,
        filter=args.filter,
        path=args.path,
        human_readable=args.human_readable,
    )
    if not content:
        raise NoContentException("No content was found. Try with different filters")
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
