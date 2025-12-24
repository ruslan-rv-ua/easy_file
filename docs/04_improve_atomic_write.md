# Improve `atomic_write` Arguments

## Context
The `atomic_write` context manager is a powerful feature for safe file operations. However, currently it only accepts `mode` and `encoding`. It does not expose other standard file opening parameters like `newline`, `errors`, or `buffering`.

## Issue
- **Newline Handling**: Users cannot control newline translation (e.g., `newline=''`) which is crucial for CSVs or specific cross-platform text files.
- **Error Handling**: Users cannot specify `errors='ignore'` or `errors='replace'`.

## Recommendation
Update `atomic_write` to accept common file opening arguments and pass them to `tempfile.NamedTemporaryFile`.

## Proposed Implementation

```python
    @contextmanager
    def atomic_write(
        self, 
        mode: str = "w", 
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
        **kwargs: Any
    ) -> Any:
        """Context manager for atomic file writes.

        Args:
            mode: File opening mode (default: 'w')
            encoding: Text encoding (defaults to UTF-8 for text modes)
            errors: Error handling strategy
            newline: Newline translation mode
            **kwargs: Additional arguments for tempfile.NamedTemporaryFile
        """
        if encoding is None and "b" not in mode:
            encoding = "utf-8"

        self.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode=mode,
            dir=self.parent,
            prefix=f".{self.name}.",
            encoding=encoding,
            errors=errors,
            newline=newline,
            delete=False,
            **kwargs
        ) as tmp_file:
            # ... existing logic
```

This ensures consistency with `open` and gives users full control over the writing process while maintaining atomicity.
