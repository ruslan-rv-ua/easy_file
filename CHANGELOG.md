# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `copy_async()` - async file copying
- `append_text_async()` - async text appending
- `read_bytes_async()` / `write_bytes_async()` - async binary operations
- `move()` / `move_async()` - move/rename files with auto parent directory creation
- `indent` parameter to `dump_json()` and `dump_json_async()` for JSON formatting control

### Changed
- Replaced `aiofiles` with `asyncio.to_thread()` for better compatibility and fewer dependencies
- Replaced deprecated `asyncio.get_event_loop()` with `asyncio.to_thread()` (Python 3.12+ compatibility)

### Fixed
- `write_text()` / `write_bytes()` now create parent directories automatically (as documented)
- `write_text_async()` / `write_bytes_async()` now create parent directories automatically
- `dump_json()` properly formats JSON with indentation by default (2 spaces)
- `copy()` / `copy_async()` return `File` object for fluent API
- Added missing `FileNotFoundError` docs to `load_json()`, `load_yaml()`, `load_json_async()`, `load_yaml_async()`

## [0.2.0] - 2025-12-23

### Added
- Typed deserialization with `dataclasses` and `TypedDict` for JSON/YAML
- Custom exceptions: `FileOperationError`, `JSONDecodeError`, `YAMLDecodeError`
- Atomic writes for `dump_json()` and `dump_yaml()`
- `atomic_write()` context manager
- Async methods: `read_text_async()`, `write_text_async()`, `load_json_async()`, `dump_json_async()`, `load_yaml_async()`, `dump_yaml_async()`
- `append_text()` utility method
- `touch_parents()` - create file and parent directories
- `size` property

### Changed
- **Breaking**: Replaced `orjson` with `msgspec` (~1.5-2× faster)
- **Breaking**: Replaced `strictyaml` with `msgspec.yaml`
- Reduced to single dependency: `msgspec`

## [0.1.0] - 2025-12-20

### Added
- Initial release
- `File` class extending `pathlib.Path`
- UTF-8 default encoding
- `open()`, `copy()`, `load_json()`, `dump_json()`, `load_yaml()`, `dump_yaml()`
- Automatic directory creation on write
- Full `pathlib.Path` compatibility

### Dependencies
- `orjson` for JSON
- `strictyaml` for YAML

[Unreleased]: https://github.com/ruslan-rv-ua/easy_file/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/ruslan-rv-ua/easy_file/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ruslan-rv-ua/easy_file/releases/tag/v0.1.0