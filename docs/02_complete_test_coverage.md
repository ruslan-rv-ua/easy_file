# Complete Test Coverage

## Context
A review of the test suite reveals that while core functionality is well-tested, several public API methods—particularly asynchronous ones and file movement operations—are completely missing tests.

## Missing Coverage
The following methods in `src/easy_file/easy_file.py` have **0% test coverage**:

### Asynchronous Byte/Text Operations
- `read_bytes_async()`
- `write_bytes_async()`
- `append_text_async()`

### File Movement
- `move()`
- `move_async()`

### Other Async Wrappers
- `copy_async()`

## Recommendation
Implement comprehensive tests for these methods in `tests/test_easy_file.py` to ensure API reliability.

## Proposed Test Cases

### 1. Test `move` and `move_async`
- **Standard Move**: Move a file from A to B and verify A is gone and B validates.
- **Cross-Device Move**: `shutil.move` behaves differently across devices; while hard to unit test easily, ensuring the wrapper calls it correctly is enough.
- **Overwrite Behavior**: Test moving to an existing path (should likely overwrite or error depending on implementation).

### 2. Test Async Byte Operations
- **Roundtrip**: Write bytes with `write_bytes_async` and read back with `read_bytes_async`.
- **Concurrency**: Ensure multiple async calls don't block the event loop (basic check).

### 3. Test `copy_async` and `append_text_async`
- **Copy**: Async copy file and verify content.
- **Append**: Async append to existing file and verify total content.

## Importance
High. These are public API endpoints. Users relying on the async capabilities for performance (the library's key selling point) may encounter unchecked bugs.
