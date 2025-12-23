# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-12-23

### Added
- Initial release of Easy File
- [`File`](src/easy_file/easy_file.py:17) class extending `pathlib.Path`
- UTF-8 default encoding for text file operations
- [`open()`](src/easy_file/easy_file.py:24) method with automatic UTF-8 encoding
- [`copy()`](src/easy_file/easy_file.py:48) method for file copying
- [`load_json()`](src/easy_file/easy_file.py:58) method for JSON deserialization using orjson
- [`dump_json()`](src/easy_file/easy_file.py:66) method for JSON serialization with formatting
- [`load_yaml()`](src/easy_file/easy_file.py:75) method for YAML deserialization using StrictYAML
- [`dump_yaml()`](src/easy_file/easy_file.py:90) method for YAML serialization
- Automatic directory creation when writing files
- Full compatibility with all `pathlib.Path` methods

### Features
- Fast JSON operations powered by [orjson](https://github.com/ijl/orjson)
- YAML operations with optional schema validation via [StrictYAML](https://github.com/crdoconnor/strictyaml)
- Automatic parent directory creation for write operations
- Binary and text mode support

### Dependencies
- orjson for JSON serialization/deserialization
- strictyaml for YAML operations

## [Unreleased]

### Planned
- Additional file format support (CSV, TOML, etc.)
- File watching capabilities
- Async file operations
- Extended error handling