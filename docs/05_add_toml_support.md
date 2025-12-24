# Add TOML Support

## Context
TOML (Tom's Obvious, Minimal Language) is becoming a standard for configuration files in the Python ecosystem (e.g., `pyproject.toml`). Since `easy_file` already supports generic configuration formats like JSON and YAML, TOML is a natural addition.

## Recommendation
Implement `load_toml` and `dump_toml` methods mirroring the existing JSON/YAML implementations. Utilize `msgspec.toml` for high-performance serialization and deserialization.

## Proposed Implementation

```python
    @overload
    def load_toml(self) -> Any: ...

    @overload
    def load_toml(self, type: type[_T]) -> _T: ...

    def load_toml(self, type: type[_T] | None = None) -> Any:
        """Load TOML data from this file.

        Args:
            type: Optional type for typed deserialization.

        Returns:
            Parsed TOML data.
        """
        try:
            content = self.read_bytes()
            if type is not None:
                return msgspec.toml.decode(content, type=type)
            return msgspec.toml.decode(content)
        except msgspec.DecodeError as e:
            # You might need to define TOMLDecodeError
            raise FileOperationError(f"Failed to decode TOML from {self}: {e}") from e

    def dump_toml(self, data: Any) -> None:
        """Dump data to this file as TOML.
        
        Uses atomic writes.
        """
        self.parent.mkdir(parents=True, exist_ok=True)
        toml_bytes = msgspec.toml.encode(data)

        with self.atomic_write(mode="wb") as f:
            f.write(toml_bytes)
```

Also add generic `load` method that picks the format based on file extension? (Optional, maybe for a separate recommendation).

## Dependencies
Ensure `msgspec` includes TOML support. Default `msgspec` installation usually includes it, but check if any extras are needed.
