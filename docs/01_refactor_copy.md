# Refactor `copy` Method

## Context
The current implementation of the `copy` method reads the entire file content into memory using `read_bytes()` and then writes it to the destination using `write_bytes()`.

```python
    def copy(self, target_path: str | pathlib.Path) -> File:
        # ...
        target.write_bytes(self.read_bytes())
        return target
```

## Issue
- **High Memory Usage**: For large files, this loads the entire file into RAM, which can cause `MemoryError` or performance degradation.
- **Performance**: It misses out on operating system optimizations (like `sendfile` on Linux/Unix) that `shutil` utilizes.

## Recommendation
Use `shutil.copy2` from the standard library. It handles metadata preservation (timestamps, permissions) and copies data efficiently without loading it all into memory.

## Proposed Implementation

```python
import shutil

    def copy(self, target_path: str | pathlib.Path, preserve_metadata: bool = True) -> File:
        """Copy this file to the target path.

        Args:
            target_path: Destination path for the copy
            preserve_metadata: Whether to preserve file metadata (timestamps, permissions). 
                               Defaults to True (uses shutil.copy2). 
                               If False, uses shutil.copy.

        Returns:
            File object for the target path
        """
        target = File(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        
        if preserve_metadata:
            shutil.copy2(self, target)
        else:
            shutil.copy(self, target)
            
        return target
```

## Benefits
- **Memory Efficient**: Streams data instead of loading everything.
- **Faster**: Utilizes OS-level copy mechanisms.
- **Metadata**: `shutil.copy2` preserves file creation/modification times and permissions, which users typically expect from a "copy" operation.
