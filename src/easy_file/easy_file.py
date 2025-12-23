"""Easy File - Files for humans."""

from __future__ import annotations

import pathlib
from typing import Any, BinaryIO, TextIO

import orjson
from strictyaml import (
    as_document,  # type: ignore[import-untyped]
)
from strictyaml import (
    load as yaml_load,  # type: ignore[import-untyped]
)


class File(pathlib.Path):
    """Extended Path class with convenient file operations.

    Provides methods for JSON and YAML operations, copying, and
    UTF-8 default encoding for text files.

    Example:
        >>> from easy_file import File
        >>> f = File("data.txt")
        >>> f.write_text("Hello, world!")
        >>> f.read_text()
        'Hello, world!'
    """

    def open(  # type: ignore[override]
        self,
        mode: str = "r",
        buffering: int = -1,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> TextIO | BinaryIO:
        """Open the file with UTF-8 default encoding for text modes.

        Args:
            mode: File opening mode ('r', 'w', 'rb', 'wb', etc.)
            buffering: Buffering policy (-1 for default)
            encoding: Text encoding (defaults to UTF-8 for text modes)
            errors: Error handling strategy
            newline: Newline handling

        Returns:
            File object (TextIO or BinaryIO)

        Example:
            >>> f = File("example.txt")
            >>> with f.open("w") as file:
            ...     file.write("Привіт світ!")
            >>> with f.open() as file:
            ...     content = file.read()
            >>> print(content)
            Привіт світ!
        """
        if encoding is None and "b" not in mode:
            encoding = "utf-8"
        return super().open(mode, buffering, encoding, errors, newline)  # type: ignore[return-value]

    def copy(self, target_path: str | pathlib.Path) -> None:
        """Copy this file to the target path.

        Args:
            target_path: Destination path for the copy

        Example:
            >>> source = File("source.txt")
            >>> source.write_text("Original content")
            >>> source.copy("backup.txt")
            >>> File("backup.txt").read_text()
            'Original content'
        """
        target = File(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(self.read_bytes())

    def load_json(self) -> Any:
        """Load JSON data from this file.

        Returns:
            Parsed JSON data (dict, list, or other JSON-compatible type)

        Example:
            >>> config = File("config.json")
            >>> config.dump_json({"name": "Easy File", "version": "0.4.0"})
            >>> data = config.load_json()
            >>> print(data)
            {'name': 'Easy File', 'version': '0.4.0'}
        """
        return orjson.loads(self.read_bytes())

    def dump_json(self, data: Any) -> None:
        """Dump data to this file as formatted JSON.

        Args:
            data: Data to serialize as JSON

        Example:
            >>> config = File("config.json")
            >>> config.dump_json({"name": "Easy File", "version": "0.4.0"})
            >>> config.read_text()
            '{\\n  "name": "Easy File",\\n  "version": "0.4.0"\\n}'
        """
        self.parent.mkdir(parents=True, exist_ok=True)
        self.write_bytes(orjson.dumps(data, option=orjson.OPT_INDENT_2))

    def load_yaml(self, schema: Any | None = None) -> Any:
        """Load YAML data from this file using StrictYAML.

        Args:
            schema: Optional StrictYAML schema for validation.
                    If None, loads as generic YAML.

        Returns:
            Parsed YAML data (StrictYAML object if schema provided, dict otherwise)

        Example:
            >>> settings = File("settings.yaml")
            >>> settings.dump_yaml({"debug": True, "port": 8080})
            >>> data = settings.load_yaml()
            >>> print(data)
            {'debug': True, 'port': 8080}

        Example with schema:
            >>> from strictyaml import Int, Map, Str
            >>> schema = Map({"name": Str(), "value": Int()})
            >>> settings.dump_yaml({"name": "test", "value": 42})
            >>> data = settings.load_yaml(schema)
            >>> print(data["name"])
            test
        """
        with self.open() as f:
            content = f.read()

        return yaml_load(content, schema) if schema is not None else yaml_load(content)

    def dump_yaml(self, data: Any, schema: Any | None = None) -> None:
        """Dump data to this file as YAML using StrictYAML.

        Args:
            data: Data to serialize as YAML
            schema: Optional StrictYAML schema for validation

        Example:
            >>> settings = File("settings.yaml")
            >>> settings.dump_yaml({"debug": True, "port": 8080})
            >>> settings.read_text()
            'debug: true\\nport: 8080\\n'

        Example with schema:
            >>> from strictyaml import Int, Map, Str
            >>> schema = Map({"name": Str(), "value": Int()})
            >>> settings.dump_yaml({"name": "test", "value": 42}, schema)
            >>> settings.read_text()
            'name: test\\nvalue: 42\\n'
        """
        self.parent.mkdir(parents=True, exist_ok=True)
        doc = as_document(data, schema)

        with self.open(mode="w") as f:
            f.write(doc.as_yaml())
