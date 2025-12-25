# Easy File

<p align="center">
<a href="https://pypi.python.org/pypi/easy_file">
    <img src="https://img.shields.io/pypi/v/easy_file.svg" alt="Release Status">
</a>
<a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
</a>
</p>

**Files for humans.**

Easy File extends Python's `pathlib.Path` to provide a more convenient, robust, and feature-rich interface for file operations.

## Features

* **Pathlib based**: Inherits all standard `pathlib.Path` operations.
* **UTF-8 by default**: No more encoding headaches; text operations default to UTF-8.
* **Fast Serialization**: Blazing fast JSON and YAML serialization using [msgspec](https://github.com/jcrist/msgspec).
* **Typed Deserialization**: Support for `TypedDict` and `dataclasses` for type-safe data loading.
* **Atomic Writes**: guarantees data integrity by writing to a temporary file first.
* **Async Support**: Full suite of async methods for non-blocking I/O.
* **Automatic Directories**: Automatically creates parent directories when writing files.
* **Robust Error Handling**: Custom exceptions for clear failure modes.

## Installation

```bash
pip install easy_file
```

## Quick Start

```python
from easy_file import File

# File operations with UTF-8 by default
f = File("data.txt")
f.write_text("Hello World!")
content = f.read_text()  # "Hello World!"

# JSON operations
config = File("config.json")
config.dump_json({"name": "My App", "version": "1.0.0"})
data = config.load_json()  # {"name": "My App", "version": "1.0.0"}

# YAML operations
settings = File("settings.yaml")
settings.dump_yaml({"debug": True, "port": 8080})
yaml_data = settings.load_yaml()  # {"debug": True, "port": 8080}

# Copy and Move
source = File("source.txt").write_text("content")
backup = source.copy("backup.txt")
moved = source.move("renamed.txt")

# All pathlib.Path methods are available
f = File("path/to/file.txt")
print(f.name)      # "file.txt"
print(f.parent)    # "path/to"
print(f.suffix)    # ".txt"
```

## Advanced Usage

### Typed Deserialization

Easy File supports typed deserialization for JSON and YAML using `TypedDict` and `dataclasses`. This provides IDE autocompletion and runtime validation.

#### Using TypedDict

```python
from typing import TypedDict
from easy_file import File

class Config(TypedDict):
    name: str
    version: str
    debug: bool

config = File("config.json")
config.dump_json({"name": "My App", "version": "1.0.0", "debug": True})

# Typed deserialization
data: Config = config.load_json(Config)
print(data["name"])  # "My App"
```

#### Using Dataclasses

```python
from dataclasses import dataclass
from easy_file import File

@dataclass
class Settings:
    debug: bool
    port: int
    host: str

settings = File("settings.yaml")
settings.dump_yaml({"debug": True, "port": 8080, "host": "localhost"})

# Typed deserialization
data: Settings = settings.load_yaml(Settings)
print(data.port)  # 8080
```

### Async Methods

Easy File provides asynchronous versions of all major I/O operations for non-blocking execution. All async methods use **aiofiles** for efficient non-blocking I/O operations.

```python
import asyncio
from easy_file import File

async def main():
    f = File("data.txt")
    
    # Text operations
    await f.write_text_async("Hello async!")
    content = await f.read_text_async()
    await f.append_text_async("\nMore content")
    
    # Binary operations
    await f.write_bytes_async(b"Binary data")
    data = await f.read_bytes_async()

    # JSON/YAML operations
    config = File("config.json")
    await config.dump_json_async({"async": True}, indent=2)
    data = await config.load_json_async()
    
    # File management
    await f.copy_async("backup.txt")
    await f.move_async("archive/data.txt")

asyncio.run(main())
```

#### Batch File Reading

Read multiple files in parallel using the `read_many_async()` class method:

```python
import asyncio
from easy_file import File

async def main():
    # Create test files
    File("file1.txt").write_text("Content 1")
    File("file2.txt").write_text("Content 2")
    File("file3.txt").write_text("Content 3")
    
    # Read all files in parallel
    paths = ["file1.txt", "file2.txt", "file3.txt"]
    contents = await File.read_many_async(paths)
    
    print(contents)  # ['Content 1', 'Content 2', 'Content 3']

asyncio.run(main())
```

This is especially useful when you need to read many files at once, as it leverages asyncio to perform all reads concurrently.

### Atomic Writes

Data integrity is crucial. Easy File uses atomic writes for `dump_json` and `dump_yaml` by default. You can also use the `atomic_write` context manager for arbitrary data.

```python
from easy_file import File

f = File("important.txt")

# Using the context manager
with f.atomic_write() as file:
    file.write("This write is atomic.")
    # If an error occurs here, the original file remains untouched.
```

### Utility Methods

Helper methods for common tasks.

* **`append_text(text)`**: Safely append text to a file.
* **`touch_parents()`**: Create a file and all necessary parent directories.
* **`size`**: Property to get file size in bytes.

```python
log = File("logs/app.log")
log.touch_parents()
log.append_text("Started.\n")
print(log.size)
```

### Error Handling

Custom exceptions help catch specific errors.

* `FileOperationError`: Base class for all Easy File errors.
* `JSONDecodeError`: Failed to decode JSON.
* `YAMLDecodeError`: Failed to decode YAML.

```python
from easy_file import File, JSONDecodeError, FileOperationError

try:
    data = File("config.json").load_json()
except JSONDecodeError:
    print("Invalid JSON format")
except FileOperationError as e:
    print(f"File error: {e}")
```

## API Reference

### Core Methods
* `File(path)`: Initialize a new File object.
* `open(mode, ...)`: Open file (defaults to UTF-8).
* `copy(target)`: Copy file to target.
* `move(target)`: Move/rename file to target.
* `touch_parents()`: Create file and parents.

### Data Methods
* `load_json(type=None)` / `dump_json(data, indent=2)`
* `load_yaml(type=None)` / `dump_yaml(data)`
* `read_text(encoding='utf-8')` / `write_text(data, ...)`
* `read_bytes()` / `write_bytes(data)`
* `append_text(text)`

### Async Methods
* `copy_async(target)` / `move_async(target)`
* `load_json_async(type=None)` / `dump_json_async(data, indent=2)`
* `load_yaml_async(type=None)` / `dump_yaml_async(data)`
* `read_text_async()` / `write_text_async(data)`
* `read_bytes_async()` / `write_bytes_async(data)`
* `append_text_async(text)`
* `read_many_async(paths)` - Class method to read multiple files in parallel

### Properties
* `size`: File size in bytes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
