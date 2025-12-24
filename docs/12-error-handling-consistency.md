# Рекомендація: Консистентність обробки помилок

## Проблема

Методи `load_json()` та `load_yaml()` обгортають помилки декодування:

```python
def load_json(self, type: type[_T] | None = None) -> Any:
    try:
        content = self.read_bytes()
        # ...
    except msgspec.DecodeError as e:
        raise JSONDecodeError(f"Failed to decode JSON from {self}: {e}") from e
```

Однак `FileNotFoundError` **не обгортається**, і це документовано лише неявно у тестах:

```python
def test_load_json_missing_file(self, temp_dir: pathlib.Path) -> None:
    """Test loading JSON from missing file raises FileNotFoundError."""
    test_file = File(temp_dir / "missing.json")
    with pytest.raises(FileNotFoundError):
        test_file.load_json()
```

## Питання для обговорення

1. **Чи потрібно обгортати `FileNotFoundError`?**
   - Поточна поведінка: пробрасується оригінальний виняток
   - Альтернатива: обгорнути у `FileOperationError`

2. **Документація винятків**
   - `load_json()` документує лише `JSONDecodeError`
   - `FileNotFoundError` не згадується в docstring

## Рекомендація

### Мінімальний варіант: Оновити документацію

```python
def load_json(self, type: type[_T] | None = None) -> Any:
    """Load JSON data from this file.

    ...

    Raises:
        JSONDecodeError: If JSON decoding fails
        FileNotFoundError: If the file doesn't exist
        
    ...
    """
```

### Розширений варіант: Обгортати всі помилки

```python
def load_json(self, type: type[_T] | None = None) -> Any:
    try:
        content = self.read_bytes()
    except FileNotFoundError as e:
        raise FileOperationError(f"File not found: {self}") from e
    
    try:
        if type is not None:
            return msgspec.json.decode(content, type=type)
        return _json_decoder.decode(content)
    except msgspec.DecodeError as e:
        raise JSONDecodeError(f"Failed to decode JSON from {self}: {e}") from e
```

## Моя рекомендація

✅ **Залишити `FileNotFoundError` без обгортання** — це стандартна поведінка Python, і користувачі очікують саме цей виняток.

❗ **Обов'язково оновити docstrings** для всіх методів, додавши `FileNotFoundError` у секцію `Raises`.

## Пріоритет

🟡 **Середній** — документація повинна відповідати поведінці.
