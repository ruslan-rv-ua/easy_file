# Рекомендація: Відсутні асинхронні методи

## Проблема

Проєкт має асинхронні версії для:
- ✅ `read_text_async()`
- ✅ `write_text_async()`
- ✅ `load_json_async()`
- ✅ `dump_json_async()`
- ✅ `load_yaml_async()`
- ✅ `dump_yaml_async()`

Але відсутні асинхронні версії для:
- ❌ `copy_async()`
- ❌ `append_text_async()`
- ❌ `read_bytes_async()`
- ❌ `write_bytes_async()`

## Рекомендація

Додати відсутні асинхронні методи для повноти API:

```python
async def copy_async(self, target_path: str | pathlib.Path) -> None:
    """Asynchronously copy this file to the target path."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, self.copy, target_path)

async def append_text_async(
    self,
    text: str,
    encoding: str = "utf-8",
    errors: str | None = None,
) -> None:
    """Asynchronously append text to this file."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, self.append_text, text, encoding, errors)

async def read_bytes_async(self) -> bytes:
    """Asynchronously read bytes from this file."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, self.read_bytes)

async def write_bytes_async(self, data: bytes) -> None:
    """Asynchronously write bytes to this file."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, self.write_bytes, data)
```

## Пріоритет

🟡 **Середній** — функціональність корисна, але не критична. Користувачі можуть обійтись поточними синхронними методами або використати `asyncio.to_thread()`.
