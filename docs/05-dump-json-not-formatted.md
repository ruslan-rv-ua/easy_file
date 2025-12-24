# Рекомендація: `dump_json()` не форматує JSON

## Проблема

У docstring методу `dump_json()` зазначено:

> "Dump data to this file as **formatted JSON**."

Приклад у документації показує:
```python
>>> config.read_text()
'{\n  "name": "Easy File",\n  "version": "0.4.0"\n}'
```

Однак реальна імплементація використовує стандартний `msgspec.json.Encoder()` без форматування:

```python
_json_encoder = msgspec.json.Encoder()
# ...
json_bytes = _json_encoder.encode(data)
```

Результат буде компактним JSON **без** відступів:
```json
{"name":"Easy File","version":"0.4.0"}
```

## Рекомендація

Для human-readable формату використовувати `msgspec.json.format()`:

```python
def dump_json(self, data: Any, indent: int = 2) -> None:
    """Dump data to this file as formatted JSON.

    Uses atomic writes to ensure data integrity.

    Args:
        data: Data to serialize as JSON
        indent: Number of spaces for indentation (default: 2).
                Set to 0 for compact output.
    """
    self.parent.mkdir(parents=True, exist_ok=True)
    json_bytes = _json_encoder.encode(data)
    
    if indent > 0:
        json_bytes = msgspec.json.format(json_bytes, indent=indent)

    # Atomic write...
```

