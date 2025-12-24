# Easy File


<p align="center">
<a href="https://pypi.python.org/pypi/easy_file">
    <img src="https://img.shields.io/pypi/v/easy_file.svg"
        alt = "Release Status">
</a>

<a href="https://github.com/ruslan-rv-ua/easy_file/actions">
    <img src="https://github.com/ruslan-rv-ua/easy_file/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">
</a>

<!-- a href="https://easy-file.readthedocs.io/en/latest/?badge=latest">
    <img src="https://readthedocs.org/projects/easy-file/badge/?version=latest" alt="Documentation Status">
</a -->

</p>


Files for humans


* Free software: MIT
* Documentation: <https://easy-file.readthedocs.io>


## Installation

```bash
pip install easy_file
```


## Quick Start

```python
from easy_file import File

# File operations with UTF-8 by default
f = File("data.txt")
f.write_text("Привіт світ!")
content = f.read_text()  # "Привіт світ!"

# JSON operations
config = File("config.json")
config.dump_json({"name": "My App", "version": "1.0.0"})
data = config.load_json()  # {"name": "My App", "version": "1.0.0"}

# YAML operations
settings = File("settings.yaml")
settings.dump_yaml({"debug": True, "port": 8080})
yaml_data = settings.load_yaml()  # {"debug": True, "port": 8080}

# Copy files
source = File("source.txt")
source.copy("backup.txt")

# All pathlib.Path methods are available
f = File("path/to/file.txt")
print(f.name)      # "file.txt"
print(f.parent)    # "path/to"
print(f.suffix)    # ".txt"
```


## Features

* based on `pathlib.Path` - all standard path operations available
* UTF-8 by default - no more encoding issues with text files
* blazing fast JSON/YAML/MessagePack serialization with [msgspec](https://github.com/jcrist/msgspec)
* typed deserialization support with dataclasses and TypedDict
* atomic writes for data safety
* async methods for non-blocking I/O
* comprehensive error handling with custom exceptions
* automatic directory creation when writing files


## Typed Deserialization

Easy File підтримує типізовану десеріалізацію JSON та YAML даних за допомогою `TypedDict` та `dataclasses`. Це забезпечує автоматичну валідацію типів та кращу підтримку IDE.

### Використання з TypedDict

```python
from typing import TypedDict
from easy_file import File

class Config(TypedDict):
    name: str
    version: str
    debug: bool

config = File("config.json")
config.dump_json({"name": "My App", "version": "1.0.0", "debug": True})

# Типізована десеріалізація
data: Config = config.load_json(Config)
print(data["name"])  # "My App"
```

### Використання з dataclasses

```python
from dataclasses import dataclass
from easy_file import File

@dataclass
class Settings:
    debug: bool
    port: int
    host: str

settings = File("settings.yaml")
settings.dump_yaml({"debug": True, "port": 8080, "host": "localhost"})

# Типізована десеріалізація
data: Settings = settings.load_yaml(Settings)
print(data.port)  # 8080
```


## Async Methods

Для неблокуючих операцій вводу-виводу Easy File надає асинхронні версії всіх основних методів.

### Асинхронне читання та запис тексту

```python
import asyncio
from easy_file import File

async def main():
    f = File("data.txt")
    await f.write_text_async("Hello async!")
    content = await f.read_text_async()
    print(content)  # "Hello async!"

asyncio.run(main())
```

### Асинхронні JSON операції

```python
import asyncio
from easy_file import File

async def main():
    config = File("config.json")
    await config.dump_json_async({"name": "My App", "version": "1.0.0"})
    data = await config.load_json_async()
    print(data)  # {"name": "Easy File", "version": "0.2.0"}

asyncio.run(main())
```

### Асинхронні YAML операції

```python
import asyncio
from easy_file import File

async def main():
    settings = File("settings.yaml")
    await settings.dump_yaml_async({"debug": True, "port": 8080})
    data = await settings.load_yaml_async()
    print(data)  # {"debug": True, "port": 8080}

asyncio.run(main())
```


## Error Handling

Easy File надає кастомні винятки для кращої обробки помилок:

- [`FileOperationError`](src/easy_file/easy_file.py:22) - базовий клас для всіх помилок операцій з файлами
- [`JSONDecodeError`](src/easy_file/easy_file.py:28) - помилка декодування JSON
- [`YAMLDecodeError`](src/easy_file/easy_file.py:34) - помилка декодування YAML

### Приклад обробки помилок

```python
from easy_file import File, JSONDecodeError, YAMLDecodeError, FileOperationError

# Обробка JSON помилок
try:
    config = File("config.json")
    data = config.load_json()
except JSONDecodeError as e:
    print(f"Помилка JSON: {e}")
except FileOperationError as e:
    print(f"Помилка файлу: {e}")

# Обробка YAML помилок
try:
    settings = File("settings.yaml")
    data = settings.load_yaml()
except YAMLDecodeError as e:
    print(f"Помилка YAML: {e}")
except FileOperationError as e:
    print(f"Помилка файлу: {e}")
```


## Atomic Writes

Easy File використовує атомарні записи для [`dump_json()`](src/easy_file/easy_file.py:150) та [`dump_yaml()`](src/easy_file/easy_file.py:226), що гарантує цілісність даних. Дані спочатку записуються у тимчасовий файл, а потім атомарно перейменовуються на цільовий файл.

### Контекстний менеджер atomic_write

Для атомарного запису будь-яких даних використовуйте контекстний менеджер [`atomic_write()`](src/easy_file/easy_file.py:257):

```python
from easy_file import File

f = File("data.txt")

# Атомарний запис тексту
with f.atomic_write() as file:
    file.write("Цей запис атомарний")

# Якщо виникне помилка в контексті, оригінальний файл не буде змінено
try:
    with f.atomic_write() as file:
        file.write("Частина даних")
        raise ValueError("Щось пішло не так")
except ValueError:
    pass  # Оригінальний файл залишається незмінним
```


## Utility Methods

Easy File надає корисні утилітарні методи для поширених операцій.

### append_text

Додає текст до кінця файлу з автоматичним створенням батьківських директорій.

```python
from easy_file import File

log = File("app.log")
log.append_text("Перший запис\n")
log.append_text("Другий запис\n")
print(log.read_text())  # "Перший запис\nДругий запис\n"
```

### touch_parents

Створює файл та всі батьківські директорії, якщо вони не існують.

```python
from easy_file import File

f = File("nested/deep/path/file.txt")
f.touch_parents()
print(f.exists())  # True
```

### size

Властивість, що повертає розмір файлу в байтах.

```python
from easy_file import File

f = File("data.txt")
f.write_text("Hello, world!")
print(f.size)  # 13 байтів
```


## API Reference

### `File(path)`

Розширений клас `pathlib.Path` зі зручними операціями з файлами.

#### Методи

| Метод | Опис |
|-------|------|
| [`open(mode, encoding, ...)`](src/easy_file/easy_file.py:54) | Відкрити файл з UTF-8 кодуванням за замовчуванням |
| [`copy(target_path)`](src/easy_file/easy_file.py:87) | Копіювати файл у цільовий шлях |
| [`load_json(type=None)`](src/easy_file/easy_file.py:110) | Завантажити JSON дані з файлу з опціональною типізацією |
| [`dump_json(data)`](src/easy_file/easy_file.py:150) | Записати дані у файл як відформатований JSON (атомарно) |
| [`load_yaml(type=None)`](src/easy_file/easy_file.py:186) | Завантажити YAML дані з файлу з опціональною типізацією |
| [`dump_yaml(data)`](src/easy_file/easy_file.py:226) | Записати дані у файл як YAML (атомарно) |
| [`atomic_write(mode, encoding)`](src/easy_file/easy_file.py:257) | Контекстний менеджер для атомарного запису |
| [`read_text_async(encoding, errors)`](src/easy_file/easy_file.py:303) | Асинхронно прочитати текст з файлу |
| [`write_text_async(data, encoding, errors)`](src/easy_file/easy_file.py:326) | Асинхронно записати текст у файл |
| [`load_json_async(type=None)`](src/easy_file/easy_file.py:355) | Асинхронно завантажити JSON дані |
| [`dump_json_async(data)`](src/easy_file/easy_file.py:382) | Асинхронно записати JSON дані |
| [`load_yaml_async(type=None)`](src/easy_file/easy_file.py:404) | Асинхронно завантажити YAML дані |
| [`dump_yaml_async(data)`](src/easy_file/easy_file.py:431) | Асинхронно записати YAML дані |
| [`append_text(text, encoding, errors)`](src/easy_file/easy_file.py:447) | Додати текст до кінця файлу |
| [`touch_parents()`](src/easy_file/easy_file.py:471) | Створити файл та батьківські директорії |

#### Властивості

| Властивість | Опис |
|-------------|------|
| [`size`](src/easy_file/easy_file.py:486) | Розмір файлу в байтах |

#### Винятки

| Виняток | Опис |
|---------|------|
| [`FileOperationError`](src/easy_file/easy_file.py:22) | Базовий клас для помилок операцій з файлами |
| [`JSONDecodeError`](src/easy_file/easy_file.py:28) | Помилка декодування JSON |
| [`YAMLDecodeError`](src/easy_file/easy_file.py:34) | Помилка декодування YAML |

Усі стандартні методи `pathlib.Path` також доступні.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

