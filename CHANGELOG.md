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
- Replaced aiofiles with asyncio.to_thread() in all async methods for better compatibility and reduced dependencies
- Replaced deprecated `asyncio.get_event_loop()` with `asyncio.to_thread()` in all async methods for Python 3.12+ compatibility

### Fixed
- Fixed `write_text()` and `write_bytes()` to create parent directories automatically as documented
- Fixed `write_text_async()` and `write_bytes_async()` to create parent directories automatically
- Improved consistency: all write methods now behave the same way regarding directory creation
- `dump_json()` now properly formats JSON with indentation by default (2 spaces), matching the documented behavior
- `copy()` and `copy_async()` methods now return a `File` object for the target path, enabling fluent API usage
- Updated README.md examples to use generic application names instead of package version numbers
- Added missing `FileNotFoundError` documentation to `load_json()`, `load_yaml()`, `load_json_async()`, and `load_yaml_async()` method docstrings

## [0.2.0] - 2025-12-23

### Added
- Typed deserialization support with dataclasses and TypedDict for JSON and YAML
- Custom exceptions: `FileOperationError`, `JSONDecodeError`, `YAMLDecodeError`
- Atomic writes for `dump_json()` and `dump_yaml()` methods
- Context manager `atomic_write()` for atomic file writes
- Async methods: `read_text_async()`, `write_text_async()`
- Async JSON methods: `load_json_async()`, `dump_json_async()`
- Async YAML methods: `load_yaml_async()`, `dump_yaml_async()`
- Utility method `append_text()` for appending text to files
- Utility method `touch_parents()` for creating file and parent directories
- Property `size` for getting file size in bytes

### Changed
- Replaced orjson with [msgspec](https://github.com/jcrist/msgspec) for JSON serialization/deserialization
- Replaced strictyaml with msgspec.yaml for YAML serialization/deserialization
- Improved performance (~1.5-2x faster for JSON/YAML operations)
- Reduced number of dependencies (single dependency: msgspec)


### Dependencies
- msgspec for JSON/YAML serialization/deserialization

## [0.1.0] - 2025-12-20

### Added
- Initial release of Easy File
- `File` class extending `pathlib.Path`
- UTF-8 default encoding for text file operations
- `open()` method with automatic UTF-8 encoding
- `copy()` method for file copying
- `load_json()` method for JSON deserialization
- `dump_json()` method for JSON serialization with formatting
- `load_yaml()` method for YAML deserialization
- `dump_yaml()` method for YAML serialization
- Automatic directory creation when writing files
- Full compatibility with all `pathlib.Path` methods

### Dependencies
- orjson for JSON serialization/deserialization
- strictyaml for YAML operations
