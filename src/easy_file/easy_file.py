"""Easy File - Files for humans."""

from __future__ import annotations

import asyncio
import pathlib
import shutil
import tempfile
from contextlib import contextmanager
from typing import Any, BinaryIO, TextIO, TypeVar, overload

import msgspec

# Global encoder and decoder for msgspec JSON
_json_encoder = msgspec.json.Encoder()
_json_decoder = msgspec.json.Decoder()
# msgspec.yaml uses encode/decode functions, not Encoder/Decoder classes

# Type variable for generic return types
_T = TypeVar("_T")


class FileOperationError(Exception):
    """Base exception for file operation errors."""

    pass


class JSONDecodeError(FileOperationError):
    """Exception raised when JSON decoding fails."""

    pass


class YAMLDecodeError(FileOperationError):
    """Exception raised when YAML decoding fails."""

    pass


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

    def copy(
        self, target_path: str | pathlib.Path, preserve_metadata: bool = True
    ) -> File:
        """Copy this file to the target path.

        Args:
            target_path: Destination path for the copy
            preserve_metadata: Whether to preserve file metadata (timestamps, permissions).
                               Defaults to True (uses shutil.copy2).
                               If False, uses shutil.copy.

        Returns:
            File object for the target path

        Example:
            >>> source = File("source.txt")
            >>> source.write_text("Original content")
            >>> backup = source.copy("backup.txt")
            >>> backup.read_text()
            'Original content'
        """
        target = File(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)

        if preserve_metadata:
            shutil.copy2(self, target)
        else:
            shutil.copy(self, target)

        return target

    def move(self, target_path: str | pathlib.Path) -> File:
        """Move this file to the target path.

        Args:
            target_path: Destination path for the move

        Returns:
            File object for the target path

        Example:
            >>> source = File("source.txt")
            >>> source.write_text("Content")
            >>> moved = source.move("target.txt")
            >>> moved.read_text()
            'Content'
            >>> source.exists()
            False
        """
        target = File(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(self), str(target))
        return target

    @overload
    def load_json(self) -> Any: ...

    @overload
    def load_json(self, type: type[_T]) -> _T: ...

    def load_json(self, type: type[_T] | None = None) -> Any:
        """Load JSON data from this file.

        Args:
            type: Optional type for typed deserialization.
                  If provided, returns data of the specified type.

        Returns:
            Parsed JSON data (dict, list, or other JSON-compatible type)
            If type is provided, returns data of the specified type.

        Raises:
            JSONDecodeError: If JSON decoding fails
            FileNotFoundError: If the file doesn't exist

        Example:
            >>> config = File("config.json")
            >>> config.dump_json({"name": "Easy File", "version": "0.4.0"})
            >>> data = config.load_json()
            >>> print(data)
            {'name': 'Easy File', 'version': '0.4.0'}

        Example with type:
            >>> from typing import TypedDict
            >>> class Config(TypedDict):
            ...     name: str
            ...     version: str
            >>> config = File("config.json")
            >>> config.dump_json({"name": "Easy File", "version": "0.4.0"})
            >>> data = config.load_json(Config)
            >>> print(data["name"])
            Easy File
        """
        try:
            content = self.read_bytes()
            if type is not None:
                return msgspec.json.decode(content, type=type)  # type: ignore[return-value]
            return _json_decoder.decode(content)
        except msgspec.DecodeError as e:
            raise JSONDecodeError(f"Failed to decode JSON from {self}: {e}") from e

    def dump_json(self, data: Any, indent: int = 2) -> None:
        """Dump data to this file as formatted JSON.

        Uses atomic writes to ensure data integrity.

        Args:
            data: Data to serialize as JSON
            indent: Number of spaces for indentation (default: 2).
                    Set to 0 for compact output.

        Example:
            >>> config = File("config.json")
            >>> config.dump_json({"name": "Easy File", "version": "0.4.0"})
            >>> config.read_text()
            '{\\n  "name": "Easy File",\\n  "version": "0.4.0"\\n}'
        """
        self.parent.mkdir(parents=True, exist_ok=True)
        json_bytes = _json_encoder.encode(data)

        if indent > 0:
            json_bytes = msgspec.json.format(json_bytes, indent=indent)

        # Atomic write using temporary file
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=self.parent,
            prefix=f".{self.name}.",
            delete=False,
        ) as tmp_file:
            tmp_path = pathlib.Path(tmp_file.name)
            tmp_file.write(json_bytes)

        # Atomic rename
        tmp_path.replace(self)

    @overload
    def load_yaml(self) -> Any: ...

    @overload
    def load_yaml(self, type: type[_T]) -> _T: ...

    def load_yaml(self, type: type[_T] | None = None) -> Any:
        """Load YAML data from this file.

        Args:
            type: Optional type for typed deserialization.
                  If provided, returns data of the specified type.

        Returns:
            Parsed YAML data (dict, list, or other YAML-compatible type)
            If type is provided, returns data of the specified type.

        Raises:
            YAMLDecodeError: If YAML decoding fails
            FileNotFoundError: If the file doesn't exist

        Example:
            >>> settings = File("settings.yaml")
            >>> settings.dump_yaml({"debug": True, "port": 8080})
            >>> data = settings.load_yaml()
            >>> print(data)
            {'debug': True, 'port': 8080}

        Example with type:
            >>> from typing import TypedDict
            >>> class Settings(TypedDict):
            ...     debug: bool
            ...     port: int
            >>> settings = File("settings.yaml")
            >>> settings.dump_yaml({"debug": True, "port": 8080})
            >>> data = settings.load_yaml(Settings)
            >>> print(data["debug"])
            True
        """
        try:
            content = self.read_bytes()
            if type is not None:
                return msgspec.yaml.decode(content, type=type)  # type: ignore[return-value]
            return msgspec.yaml.decode(content)
        except msgspec.DecodeError as e:
            raise YAMLDecodeError(f"Failed to decode YAML from {self}: {e}") from e

    def dump_yaml(self, data: Any) -> None:
        """Dump data to this file as YAML.

        Uses atomic writes to ensure data integrity.

        Args:
            data: Data to serialize as YAML

        Example:
            >>> settings = File("settings.yaml")
            >>> settings.dump_yaml({"debug": True, "port": 8080})
            >>> settings.read_text()
            'debug: true\\nport: 8080\\n'
        """
        self.parent.mkdir(parents=True, exist_ok=True)
        yaml_bytes = msgspec.yaml.encode(data)

        # Atomic write using temporary file
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=self.parent,
            prefix=f".{self.name}.",
            delete=False,
        ) as tmp_file:
            tmp_path = pathlib.Path(tmp_file.name)
            tmp_file.write(yaml_bytes)

        # Atomic rename
        tmp_path.replace(self)

    @contextmanager
    def atomic_write(self, mode: str = "w", encoding: str | None = None) -> Any:
        """Context manager for atomic file writes.

        Writes to a temporary file and atomically renames it to the target
        path when the context exits successfully.

        Args:
            mode: File opening mode (default: 'w')
            encoding: Text encoding (defaults to UTF-8 for text modes)

        Yields:
            File object for writing

        Example:
            >>> f = File("data.txt")
            >>> with f.atomic_write() as file:
            ...     file.write("Atomic content")
            >>> f.read_text()
            'Atomic content'
        """
        if encoding is None and "b" not in mode:
            encoding = "utf-8"

        self.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode=mode,
            dir=self.parent,
            prefix=f".{self.name}.",
            encoding=encoding,
            delete=False,
        ) as tmp_file:
            tmp_path = pathlib.Path(tmp_file.name)
            try:
                yield tmp_file
                tmp_file.flush()
                # Close the file before replace/unlink to avoid Windows file lock issues
                tmp_file.close()
            except Exception:
                # Close the file before unlink to avoid Windows file lock issues
                tmp_file.close()
                tmp_path.unlink(missing_ok=True)
                raise
            else:
                tmp_path.replace(self)

    async def read_text_async(
        self, encoding: str = "utf-8", errors: str | None = None
    ) -> str:
        """Asynchronously read text from this file.

        Args:
            encoding: Text encoding (default: 'utf-8')
            errors: Error handling strategy

        Returns:
            File content as string

        Example:
            >>> import asyncio
            >>> f = File("data.txt")
            >>> f.write_text("Hello")
            >>> content = asyncio.run(f.read_text_async())
            >>> print(content)
            Hello
        """
        return await asyncio.to_thread(self.read_text, encoding, errors)

    async def write_text_async(
        self,
        data: str,
        encoding: str = "utf-8",
        errors: str | None = None,
    ) -> None:
        """Asynchronously write text to this file.

        Args:
            data: Text to write
            encoding: Text encoding (default: 'utf-8')
            errors: Error handling strategy

        Example:
            >>> import asyncio
            >>> f = File("data.txt")
            >>> asyncio.run(f.write_text_async("Hello async"))
            >>> f.read_text()
            'Hello async'
        """

        def _write() -> None:
            self.parent.mkdir(parents=True, exist_ok=True)
            self.write_text(data, encoding, errors)

        await asyncio.to_thread(_write)

    @overload
    async def load_json_async(self) -> Any: ...

    @overload
    async def load_json_async(self, type: type[_T]) -> _T: ...

    async def load_json_async(self, type: type[_T] | None = None) -> Any:
        """Asynchronously load JSON data from this file.

        Args:
            type: Optional type for typed deserialization.

        Returns:
            Parsed JSON data

        Raises:
            JSONDecodeError: If JSON decoding fails
            FileNotFoundError: If the file doesn't exist

        Example:
            >>> import asyncio
            >>> config = File("config.json")
            >>> config.dump_json({"name": "Easy File"})
            >>> data = asyncio.run(config.load_json_async())
            >>> print(data)
            {'name': 'Easy File'}
        """

        def _load() -> Any:
            return self.load_json(type)  # type: ignore[arg-type]

        return await asyncio.to_thread(_load)

    async def dump_json_async(self, data: Any, indent: int = 2) -> None:
        """Asynchronously dump data to this file as formatted JSON.

        Args:
            data: Data to serialize as JSON
            indent: Number of spaces for indentation (default: 2).
                    Set to 0 for compact output.

        Example:
            >>> import asyncio
            >>> config = File("config.json")
            >>> asyncio.run(config.dump_json_async({"name": "Easy File"}))
            >>> config.read_text()
            '{\\n  "name": "Easy File"\\n}'
        """
        await asyncio.to_thread(self.dump_json, data, indent)

    @overload
    async def load_yaml_async(self) -> Any: ...

    @overload
    async def load_yaml_async(self, type: type[_T]) -> _T: ...

    async def load_yaml_async(self, type: type[_T] | None = None) -> Any:
        """Asynchronously load YAML data from this file.

        Args:
            type: Optional type for typed deserialization.

        Returns:
            Parsed YAML data

        Raises:
            YAMLDecodeError: If YAML decoding fails
            FileNotFoundError: If the file doesn't exist

        Example:
            >>> import asyncio
            >>> settings = File("settings.yaml")
            >>> settings.dump_yaml({"debug": True})
            >>> data = asyncio.run(settings.load_yaml_async())
            >>> print(data)
            {'debug': True}
        """

        def _load() -> Any:
            return self.load_yaml(type)  # type: ignore[arg-type]

        return await asyncio.to_thread(_load)

    async def dump_yaml_async(self, data: Any) -> None:
        """Asynchronously dump data to this file as YAML.

        Args:
            data: Data to serialize as YAML

        Example:
            >>> import asyncio
            >>> settings = File("settings.yaml")
            >>> asyncio.run(settings.dump_yaml_async({"debug": True}))
            >>> settings.read_text()
            'debug: true\\n'
        """
        await asyncio.to_thread(self.dump_yaml, data)

    async def copy_async(self, target_path: str | pathlib.Path) -> File:
        """Asynchronously copy this file to the target path.

        Args:
            target_path: Destination path for the copy

        Returns:
            File object for the target path

        Example:
            >>> import asyncio
            >>> source = File("source.txt")
            >>> source.write_text("Original content")
            >>> backup = asyncio.run(source.copy_async("backup.txt"))
            >>> backup.read_text()
            'Original content'
        """
        return await asyncio.to_thread(self.copy, target_path)

    async def move_async(self, target_path: str | pathlib.Path) -> File:
        """Asynchronously move this file to the target path.

        Args:
            target_path: Destination path for the move

        Returns:
            File object for the target path

        Example:
            >>> import asyncio
            >>> source = File("source.txt")
            >>> source.write_text("Content")
            >>> moved = asyncio.run(source.move_async("target.txt"))
            >>> moved.read_text()
            'Content'
        """
        return await asyncio.to_thread(self.move, target_path)

    async def append_text_async(
        self,
        text: str,
        encoding: str = "utf-8",
        errors: str | None = None,
    ) -> None:
        """Asynchronously append text to this file.

        Args:
            text: Text to append
            encoding: Text encoding (default: 'utf-8')
            errors: Error handling strategy

        Example:
            >>> import asyncio
            >>> f = File("log.txt")
            >>> f.write_text("First line\\n")
            >>> asyncio.run(f.append_text_async("Second line\\n"))
            >>> f.read_text()
            'First line\\nSecond line\\n'
        """
        await asyncio.to_thread(self.append_text, text, encoding, errors)

    async def read_bytes_async(self) -> bytes:
        """Asynchronously read bytes from this file.

        Returns:
            File content as bytes

        Example:
            >>> import asyncio
            >>> f = File("data.bin")
            >>> f.write_bytes(b"\\x00\\x01\\x02")
            >>> content = asyncio.run(f.read_bytes_async())
            >>> print(content)
            b'\\x00\\x01\\x02'
        """
        return await asyncio.to_thread(self.read_bytes)

    async def write_bytes_async(self, data: bytes) -> None:
        """Asynchronously write bytes to this file.

        Args:
            data: Bytes to write

        Example:
            >>> import asyncio
            >>> f = File("data.bin")
            >>> asyncio.run(f.write_bytes_async(b"\\x00\\x01\\x02"))
            >>> f.read_bytes()
            b'\\x00\\x01\\x02'
        """

        def _write() -> None:
            self.parent.mkdir(parents=True, exist_ok=True)
            self.write_bytes(data)

        await asyncio.to_thread(_write)

    def append_text(
        self,
        text: str,
        encoding: str = "utf-8",
        errors: str | None = None,
    ) -> None:
        """Append text to this file.

        Args:
            text: Text to append
            encoding: Text encoding (default: 'utf-8')
            errors: Error handling strategy

        Example:
            >>> f = File("log.txt")
            >>> f.write_text("First line\\n")
            >>> f.append_text("Second line\\n")
            >>> f.read_text()
            'First line\\nSecond line\\n'
        """
        self.parent.mkdir(parents=True, exist_ok=True)
        with self.open(mode="a", encoding=encoding, errors=errors) as f:
            f.write(text)  # type: ignore[arg-type]

    def touch_parents(self) -> None:
        """Create this file and all parent directories if they don't exist.

        Similar to `touch` command but also creates parent directories.

        Example:
            >>> f = File("nested/deep/file.txt")
            >>> f.touch_parents()
            >>> f.exists()
            True
        """
        self.parent.mkdir(parents=True, exist_ok=True)
        self.touch()

    @property
    def size(self) -> int:
        """Get the size of this file in bytes.

        Returns:
            File size in bytes

        Raises:
            FileNotFoundError: If the file doesn't exist

        Example:
            >>> f = File("data.txt")
            >>> f.write_text("Hello")
            >>> f.size
            5
        """
        return self.stat().st_size
