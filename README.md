# Easy File


<p align="center">
<a href="https://pypi.python.org/pypi/easy_file">
    <img src="https://img.shields.io/pypi/v/easy_file.svg"
        alt = "Release Status">
</a>

<a href="https://github.com/ruslan-rv-ua/easy_file/actions">
    <img src="https://github.com/ruslan-rv-ua/easy_file/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">
</a>

<!-- a href="https://easy-file.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/easy-file/badge/?version=latest" alt="Documentation Status">
</a -->

</p>


Files for humans


* Free software: MIT
* Documentation: <https://easy-file.readthedocs.io>


## Installation

```bash
pip install easy_file
```


## Quick Start

```python
from easy_file import File

# File operations with UTF-8 by default
f = File("data.txt")
f.write_text("Привіт світ!")
content = f.read_text()  # "Привіт світ!"

# JSON operations
config = File("config.json")
config.dump_json({"name": "Easy File", "version": "0.4.0"})
data = config.load_json()  # {"name": "Easy File", "version": "0.4.0"}

# YAML operations
settings = File("settings.yaml")
settings.dump_yaml({"debug": True, "port": 8080})
yaml_data = settings.load_yaml()  # {"debug": True, "port": 8080}

# Copy files
source = File("source.txt")
source.copy("backup.txt")

# All pathlib.Path methods are available
f = File("path/to/file.txt")
print(f.name)      # "file.txt"
print(f.parent)    # "path/to"
print(f.suffix)    # ".txt"
```


## Features

* based on `pathlib.Path` - all standard path operations available
* UTF-8 by default - no more encoding issues with text files
* fast JSON serialization/deserialization with [orjson](https://github.com/ijl/orjson)
* YAML serialization/deserialization with [StrictYAML](https://github.com/crdoconnor/strictyaml)
* automatic directory creation when writing files


## API Reference

### `File(path)`

Extended `pathlib.Path` class with convenient file operations.

#### Methods

| Method | Description |
|--------|-------------|
| [`open(mode, encoding, ...)`](src/easy_file/easy_file.py:24) | Open file with UTF-8 default encoding |
| [`copy(target_path)`](src/easy_file/easy_file.py:48) | Copy file to target path |
| [`load_json()`](src/easy_file/easy_file.py:58) | Load JSON data from file |
| [`dump_json(data)`](src/easy_file/easy_file.py:66) | Dump data to file as formatted JSON |
| [`load_yaml(schema=None)`](src/easy_file/easy_file.py:75) | Load YAML data with optional schema validation |
| [`dump_yaml(data, schema=None)`](src/easy_file/easy_file.py:90) | Dump data to file as YAML with optional schema validation |

All standard `pathlib.Path` methods are also available.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.
