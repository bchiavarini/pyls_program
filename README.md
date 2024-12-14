## Python Command Line Tool for listing directory contents

### Setup
1. Ensure that Python is installed on your system and that the `python3` command works properly
2. Create a JSON file describing your directory structure with the following schema:
```json
{
  "name": "string",
  "size": "integer",
  "time_modified": "epoch time",
  "permissions": "Unix-like permissions",
  "contents": [
    {
      "name": "string",
      "size": "integer",
      "time_modified": "epoch time",
      "permissions": "Unix-like permissions"
    },
    {
      "name": "string",
      "size": "integer",
      "time_modified": "epoch time",
      "permissions": "Unix-like permissions"
    }
  ]
}
```
3. Save the file as _structure.json_ and place it in the _pyls_ folder. An example JSON file is already provided in the project to help you get started. 
4. If you want to use a custom filename or filepath for your JSON file, update the `CONFIG_FILEPATH` variable in `pyls.py` accordingly.

### Usage
1. Navigate to the _pyls_ folder
2. Run the following command
``` bash
python3 -m pyls
```
The program will list the content of the directory described in the JSON file. Note that hidden directories will not be displayed.