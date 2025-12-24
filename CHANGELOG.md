# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added `copy_async()` method for asynchronous file copying
- Added `append_text_async()` method for asynchronous text appending
- Added `read_bytes_async()` method for asynchronous byte reading
- Added `write_bytes_async()` method for asynchronous byte writing
- Added `indent` parameter to `dump_json()` and `dump_json_async()` methods for controlling JSON formatting
- Added `move()` and `move_async()` methods for moving/renaming files with automatic parent directory creation

### Changed
- Replaced deprecated `asyncio.get_event_loop()` with `asyncio.to_thread()` in all async methods for Python 3.12+ compatibility
- `dump_json()` now properly formats JSON with indentation by default (2 spaces), matching the documented behavior
- `copy()` and `copy_async()` methods now return a `File` object for the target path, enabling fluent API usage

## [0.2.0] - 2025-12-23

### Added
- Typed deserialization support with dataclasses and TypedDict for JSON and YAML
- Custom exceptions: [`FileOperationError`](src/easy_file/easy_file.py:22), [`JSONDecodeError`](src/easy_file/easy_file.py:28), [`YAMLDecodeError`](src/easy_file/easy_file.py:34)
- Atomic writes for [`dump_json()`](src/easy_file/easy_file.py:150) and [`dump_yaml()`](src/easy_file/easy_file.py:226) methods
- Context manager [`atomic_write()`](src/easy_file/easy_file.py:257) for atomic file writes
- Async methods: [`read_text_async()`](src/easy_file/easy_file.py:303), [`write_text_async()`](src/easy_file/easy_file.py:326)
- Async JSON methods: [`load_json_async()`](src/easy_file/easy_file.py:355), [`dump_json_async()`](src/easy_file/easy_file.py:382)
- Async YAML methods: [`load_yaml_async()`](src/easy_file/easy_file.py:404), [`dump_yaml_async()`](src/easy_file/easy_file.py:431)
- Utility method [`append_text()`](src/easy_file/easy_file.py:447) for appending text to files
- Utility method [`touch_parents()`](src/easy_file/easy_file.py:471) for creating file and parent directories
- Property [`size`](src/easy_file/easy_file.py:486) for getting file size in bytes

### Changed
- Replaced orjson with [msgspec](https://github.com/jcrist/msgspec) for JSON serialization/deserialization
- Replaced strictyaml with msgspec.yaml for YAML serialization/deserialization
- Improved performance (~1.5-2x faster for JSON/YAML operations)
- Reduced number of dependencies (single dependency: msgspec)

### Features
- Blazing fast JSON/YAML/MessagePack serialization powered by msgspec
- Type-safe deserialization with automatic validation
- Non-blocking async I/O operations
- Data integrity guaranteed by atomic writes
- Comprehensive error handling with custom exceptions

### Dependencies
- msgspec for JSON/YAML serialization/deserialization

## [0.1.0] - 2025-12-23

### Added
- Initial release of Easy File
- [`File`](src/easy_file/easy_file.py:40) class extending `pathlib.Path`
- UTF-8 default encoding for text file operations
- [`open()`](src/easy_file/easy_file.py:54) method with automatic UTF-8 encoding
- [`copy()`](src/easy_file/easy_file.py:87) method for file copying
- [`load_json()`](src/easy_file/easy_file.py:110) method for JSON deserialization
- [`dump_json()`](src/easy_file/easy_file.py:150) method for JSON serialization with formatting
- [`load_yaml()`](src/easy_file/easy_file.py:186) method for YAML deserialization
- [`dump_yaml()`](src/easy_file/easy_file.py:226) method for YAML serialization
- Automatic directory creation when writing files
- Full compatibility with all `pathlib.Path` methods

### Dependencies
- orjson for JSON serialization/deserialization
- strictyaml for YAML operations

## [Unreleased]

### Planned
- Additional file format support (CSV, TOML, etc.)
- File watching capabilities
- Extended error handling
- Performance optimizations