# Рекомендація: Покращення Type Hints

## Проблема 1: Використання `Any` у return types

Методи `load_json()` та `load_yaml()` повертають `Any`:

```python
def load_json(self, type: type[_T] | None = None) -> Any:
    ...
```

Це знижує корисність type checking.

## Рекомендація 1: Перевантаження з @overload

Поточні `@overload` декларації правильні, але можна покращити базовий випадок:

```python
from typing import overload, Any, TypeVar

_T = TypeVar("_T")

@overload
def load_json(self) -> dict[str, Any]: ...

@overload
def load_json(self, type: type[_T]) -> _T: ...

def load_json(self, type: type[_T] | None = None) -> Any:
    ...
```

Тепер `load_json()` без аргументів повертає `dict[str, Any]` замість `Any`.

## Проблема 2: Параметр `type` конфліктує з builtin

Ім'я параметра `type` перекриває вбудовану функцію `type()`:

```python
def load_json(self, type: type[_T] | None = None) -> Any:
    # `type` тут — це параметр, не builtin
```

## Рекомендація 2: Перейменувати параметр

```python
def load_json(self, target_type: type[_T] | None = None) -> Any:
    """Load JSON data from this file.

    Args:
        target_type: Optional type for typed deserialization.
    """
```

Альтернативи:
- `schema`
- `as_type`
- `decode_type`

## Проблема 3: Return type для `atomic_write`

```python
@contextmanager
def atomic_write(self, mode: str = "w", encoding: str | None = None) -> Any:
```

`Any` занадто широкий.

## Рекомендація 3: Використати Generator type

```python
from typing import Generator
from contextlib import contextmanager

@contextmanager
def atomic_write(
    self, mode: str = "w", encoding: str | None = None
) -> Generator[TextIO | BinaryIO, None, None]:
    ...
```

## Пріоритет

🟡 **Середній** — покращує developer experience та IDE support.
