## Python Command Line Tool for listing directory contents

### Setup
1. Clone this project
```bash
git clone https://github.com/bchiavarini/pyls_program.git
```
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
5. Create a virtual environment (if you use a virtual environment)
```bash
python3 -mvenv .venv
source .venv/bin/activate
```
6. Install the project and its dependencies
```bash
pip install .
```


### Usage
1. Run the following command
``` bash
pyls
```
The program will list the contents of the directory described in the your _structure.json_ (or the file specified in your custom `CONFIG_FILEPATH` variable).\
Note that, if no additional parameters are specified, hidden directories will not be displayed.
2. To see a list of all available options and their descriptions, you can use the `--help` flag:
``` bash
pyls --help
```
3. To change the directory structure to be parsed, update your _structure.json_ (or the file specified in your custom `CONFIG_FILEPATH` variable) accordingly