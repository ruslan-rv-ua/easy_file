# Рекомендація: Метод `copy()` не повертає цільовий файл

## Проблема

Метод `copy()` повертає `None`:

```python
def copy(self, target_path: str | pathlib.Path) -> None:
    """Copy this file to the target path."""
    target = File(target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(self.read_bytes())
```

Це не дозволяє створювати fluent/chain-style API:

```python
# Поточний спосіб
source.copy("backup.txt")
backup = File("backup.txt")
backup.read_text()

# Бажаний спосіб (fluent API)
content = source.copy("backup.txt").read_text()
```

## Рекомендація

Повертати `File` об'єкт для цільового файлу:

```python
def copy(self, target_path: str | pathlib.Path) -> "File":
    """Copy this file to the target path.

    Args:
        target_path: Destination path for the copy

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
    target.write_bytes(self.read_bytes())
    return target
```

## Переваги

1. **Fluent API**: дозволяє chain-виклики
2. **Зручність**: не потрібно створювати новий `File` об'єкт
3. **Консистентність**: схоже на `shutil.copy()` який повертає шлях

## Пріоритет

🟢 **Низький** — покращення зручності, але не критичне.
