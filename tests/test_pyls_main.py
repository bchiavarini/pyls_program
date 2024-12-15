import json
import sys
from pathlib import Path

import pytest

from pyls import (
    CONFIG_FILEPATH,
    ArgsValidationException,
    JsonDecoderException,
    NoContentException,
    main,
)


def restore_original_config_file(filename: str):
    file_to_restore = Path(filename)
    if file_to_restore.is_file():
        file_to_restore.rename(CONFIG_FILEPATH)


def rename_config_file(temp_name: str):
    config_file = Path(CONFIG_FILEPATH)
    if config_file.is_file():
        # rename the config file
        config_file.rename(temp_name)


def test_config_file_not_found():
    # simulate the config file does not exist moving it
    temp_name = f"{CONFIG_FILEPATH}_bk"
    rename_config_file(temp_name)

    # pass no arguments to prevent main failure
    sys.argv = []
    # test case of a not existing structure json
    try:
        with pytest.raises(FileNotFoundError, match="structure.json not found"):
            main()
    finally:
        # restore the original file
        restore_original_config_file(temp_name)


def test_config_file_malformed():
    # save the original file with a different name
    temp_name = f"{CONFIG_FILEPATH}_bk"
    rename_config_file(temp_name)
    # create a malformed config file
    malformed_json = '{"contents": [ { "name": "file1.txt", }'
    config_file = Path(CONFIG_FILEPATH)
    with config_file.open("w") as f:
        f.write(malformed_json)
    try:
        with pytest.raises(JsonDecoderException):
            main()
    finally:
        # restore the original file
        restore_original_config_file(temp_name)


def test_reverse_function(capfd):
    # save the original file with a different name
    temp_name = f"{CONFIG_FILEPATH}_bk"
    rename_config_file(temp_name)
    # create a mocked config file
    mocked_json = {"contents": [{"name": "file1.txt"}, {"name": "file2.txt"}]}
    config_file = Path(CONFIG_FILEPATH)
    with config_file.open("w") as f:
        json.dump(mocked_json, f)
    try:
        sys.argv = ["pyls.py", "-r"]
        main()
        output = capfd.readouterr()
        assert output.out.strip() == "file2.txt file1.txt"
    finally:
        # restore the original file
        restore_original_config_file(temp_name)


def test_validation_for_filter_param():
    sys.argv = ["pyls.py", "--filter", "folder"]
    # test case of a not existing structure json
    with pytest.raises(ArgsValidationException):
        main()


def test_filters_without_results():
    # save the original file with a different name
    temp_name = f"{CONFIG_FILEPATH}_bk"
    rename_config_file(temp_name)
    # create a mocked config file
    mocked_json = {
        "contents": [{"name": "folder1", "contents": [{"name": "file2.txt"}]}]
    }
    config_file = Path(CONFIG_FILEPATH)
    with config_file.open("w") as f:
        json.dump(mocked_json, f)
    sys.argv = ["pyls.py", "--filter", "dir", "folder1"]
    # test case of a not existing structure json
    try:
        with pytest.raises(NoContentException):
            main()
    finally:
        # restore the original file
        restore_original_config_file(temp_name)
