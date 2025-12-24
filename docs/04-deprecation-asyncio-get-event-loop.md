# Рекомендація: Застаріле використання `asyncio.get_event_loop()`

## Проблема

В асинхронних методах використовується `asyncio.get_event_loop()`:

```python
async def read_text_async(self, encoding: str = "utf-8", errors: str | None = None) -> str:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, self.read_text, encoding, errors)
```

Починаючи з Python 3.10, `asyncio.get_event_loop()` видає `DeprecationWarning` якщо немає запущеного event loop. У Python 3.12+ поведінка може бути ще більш обмежувальною.

## Рекомендація

Використовувати `asyncio.get_running_loop()` замість `asyncio.get_event_loop()`:

```python
async def read_text_async(self, encoding: str = "utf-8", errors: str | None = None) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, self.read_text, encoding, errors)
```

Або ще краще — використовувати `asyncio.to_thread()` (доступний з Python 3.9):

```python
async def read_text_async(self, encoding: str = "utf-8", errors: str | None = None) -> str:
    return await asyncio.to_thread(self.read_text, encoding, errors)
```

## Переваги `asyncio.to_thread()`

1. Простіший синтаксис
2. Автоматично копіює контекстні змінні
3. Більш читабельний код
4. Рекомендований спосіб з Python 3.9+

## Приклад оновленого коду

```python
async def read_text_async(
    self, encoding: str = "utf-8", errors: str | None = None
) -> str:
    return await asyncio.to_thread(self.read_text, encoding, errors)

async def write_text_async(
    self,
    data: str,
    encoding: str = "utf-8",
    errors: str | None = None,
) -> None:
    await asyncio.to_thread(self.write_text, data, encoding, errors)

async def load_json_async(self, type: type[_T] | None = None) -> Any:
    return await asyncio.to_thread(self.load_json, type)

async def dump_json_async(self, data: Any) -> None:
    await asyncio.to_thread(self.dump_json, data)
```

## Пріоритет

🔴 **Високий** — проєкт підтримує Python 3.12+, тому варто використовувати сучасні підходи та уникати deprecation warnings.
