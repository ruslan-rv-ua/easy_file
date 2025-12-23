# План повної переробки проєкту easy_file

## Огляд

Цей документ описує детальний покроковий план повної переробки проєкту `easy_file` з використанням сучасних інструментів та практик розробки.

## Цілі

1. Видалити застарілі інструменти (poetry, mkdocs, tox, flake8, isort, black)
2. Впровадити сучасні інструменти (uv, ruff, mypy, git-flow, pre-commit)
3. Зберегти функціональність класу File
4. Оновити Python версію до 3.12+
5. Створити реальні тести

---

## Етап 1: Підготовка та очищення

### 1.1 Створення резервної копії

```bash
# Створити гілку для резервної копії
git checkout -b backup-before-remake
git push origin backup-before-remake

# Повернутися на main
git checkout main
```

### 1.2 Видалення застарілих файлів та папок

```bash
# Видалити документацію mkdocs
rm -rf docs/
rm mkdocs.yml

# Видалити конфігураційні файли старих інструментів
rm tox.ini
rm .flake8
rm .isort.cfg
rm .coveragerc
rm pyrightconfig.json

# Видалити poetry файли
rm poetry.lock
# pyproject.toml буде перезаписаний пізніше
# .pre-commit-config.yaml буде перезаписаний пізніше з новим ruff
```

### 1.3 Очищення віртуальних середовищ

```bash
# Видалити старі віртуальні середовища
rm -rf .venv
rm -rf .tox
rm -rf .mypy_cache
rm -rf __pycache__
rm -rf easy_file/__pycache__
rm -rf tests/__pycache__
```

### 1.4 Оновлення .gitignore

Перевірити та оновити [`.gitignore`](../.gitignore), додати:
```
.venv/
.mypy_cache/
.ruff_cache/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
```

---

## Етап 2: Налаштування нових інструментів

### 2.1 Ініціалізація проєкту з uv

```bash
# Ініціалізувати новий проєкт
uv init --name easy_file

# Це створить новий pyproject.toml з базовою конфігурацією
```

### 2.2 Налаштування Python версії

```bash
# Встановити Python 3.12+ як версію проєкту
uv python install 3.12
uv python pin 3.12
```

### 2.3 Налаштування ruff

Конфігурація ruff буде розміщена в [`pyproject.toml`](../pyproject.toml) разом з іншими налаштуваннями проєкту.

### 2.4 Налаштування mypy

Створити файл `mypy.ini`:

```ini
[mypy]
python_version = 3.12
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
strict_equality = True

[mypy-orjson]
ignore_missing_imports = True

[mypy.strictyaml.*]
ignore_missing_imports = True
```

### 2.5 Налаштування git-flow

```bash
# Переконатися, що git-flow встановлено
# Windows: через Git Bash або Scoop
# Linux/Mac: brew install git-flow-avh

# Ініціалізувати git-flow
git-flow init

# Відповісти на запитання:
# - Branch name for production releases: main
# - Branch name for "next release" development: develop
# - Branch name for feature branches: feature/
# - Branch name for bugfix branches: bugfix/
# - Branch name for release branches: release/
# - Branch name for hotfix branches: hotfix/
# - Branch name for support tags: support/
```

---

## Етап 3: Структура проєкту

### 3.1 Нова структура файлів та папок

```
easy_file/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Новий CI workflow
│       └── release.yml     # Оновлений release workflow
├── src/
│   └── easy_file/
│       ├── __init__.py
│       └── easy_file.py    # Оновлений клас File з типізацією
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures
│   └── test_easy_file.py   # Реальні тести
├── plans/
│   └── project_remake.md   # Цей файл
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml          # Новий конфіг з uv, ruff, pytest
└── mypy.ini                # Конфігурація mypy
```

### 3.2 Створення нового pyproject.toml

```toml
[project]
name = "easy_file"
version = "0.4.0"
description = "Files for humans."
readme = "README.md"
requires-python = ">=3.12"
license = {text = "MIT"}
authors = [
    {name = "Ruslan Iskov", email = "ruslan.rv.ua@gmail.com"}
]
keywords = ["file", "pathlib", "json", "yaml"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]

dependencies = [
    "orjson>=3.9.0",
    "strictyaml>=1.7.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
    "pre-commit>=3.5.0",
]

[project.urls]
Homepage = "https://github.com/ruslan-rv-ua/easy_file"
Repository = "https://github.com/ruslan-rv-ua/easy_file"
Issues = "https://github.com/ruslan-rv-ua/easy_file/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/easy_file"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=easy_file",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
]

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
]
ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # do not perform function calls in argument defaults
    "C901",   # too complex
]

[tool.ruff.format]
indent-style = "space"
line-length = 88
quote-style = "double"
skip-magic-trailing-comma = false
```

---

## Етап 4: Міграція коду

### 4.1 Адаптація класу File з типізацією

Створити оновлений файл [`src/easy_file/easy_file.py`](../src/easy_file/easy_file.py):

```python
"""Easy File - Files for humans."""

from __future__ import annotations

import pathlib
from typing import Any, BinaryIO, TextIO, Union

import orjson
from strictyaml import YAML, load as yaml_load


class File(pathlib.Path):
    """Extended Path class with convenient file operations.
    
    Provides methods for JSON and YAML operations, copying, and
    UTF-8 default encoding for text files.
    """

    def open(
        self,
        mode: str = "r",
        buffering: int = -1,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> Union[TextIO, BinaryIO]:
        """Open the file with UTF-8 default encoding for text modes.
        
        Args:
            mode: File opening mode ('r', 'w', 'rb', 'wb', etc.)
            buffering: Buffering policy (-1 for default)
            encoding: Text encoding (defaults to UTF-8 for text modes)
            errors: Error handling strategy
            newline: Newline handling
            
        Returns:
            File object (TextIO or BinaryIO)
        """
        if encoding is None and "b" not in mode:
            encoding = "utf-8"
        return super().open(mode, buffering, encoding, errors, newline)

    def copy(self, target_path: str | pathlib.Path) -> None:
        """Copy this file to the target path.
        
        Args:
            target_path: Destination path for the copy
        """
        File(target_path).write_bytes(self.read_bytes())

    def load_json(self) -> Any:
        """Load JSON data from this file.
        
        Returns:
            Parsed JSON data (dict, list, or other JSON-compatible type)
        """
        data = orjson.loads(self.read_bytes())
        return data

    def dump_json(self, data: Any) -> None:
        """Dump data to this file as formatted JSON.
        
        Args:
            data: Data to serialize as JSON
        """
        self.write_bytes(orjson.dumps(data, option=orjson.OPT_INDENT_2))

    def load_yaml(self, schema: Any | None = None) -> Any:
        """Load YAML data from this file using StrictYAML.
        
        Args:
            schema: Optional StrictYAML schema for validation.
                    If None, loads as generic YAML.
        
        Returns:
            Parsed YAML data (StrictYAML object if schema provided, dict otherwise)
        """
        with self.open() as f:
            content = f.read()
        
        if schema is not None:
            return yaml_load(content, schema)
        return yaml_load(content)

    def dump_yaml(self, data: Any, schema: Any | None = None) -> None:
        """Dump data to this file as YAML using StrictYAML.
        
        Args:
            data: Data to serialize as YAML
            schema: Optional StrictYAML schema for validation
        """
        yaml = YAML()
        if schema is not None:
            yaml = YAML(schema)
        
        with self.open(mode="w") as f:
            yaml.dump(data, f)


if __name__ == "__main__":
    pass
```

### 4.2 Оновлення __init__.py

Створити файл [`src/easy_file/__init__.py`](../src/easy_file/__init__.py):

```python
"""Easy File - Files for humans."""

from easy_file.easy_file import File

__all__ = ["File"]
__version__ = "0.4.0"
```

### 4.3 Створення conftest.py для pytest

Створити файл [`tests/conftest.py`](../tests/conftest.py):

```python
"""Pytest configuration and shared fixtures."""

import pathlib
import tempfile
from typing import Generator

import pytest


@pytest.fixture
def temp_dir() -> Generator[pathlib.Path, None, None]:
    """Create a temporary directory for testing.
    
    Yields:
        Path to temporary directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield pathlib.Path(tmpdir)


@pytest.fixture
def sample_json_data() -> dict[str, object]:
    """Sample JSON data for testing.
    
    Returns:
        Dictionary with sample data
    """
    return {
        "name": "test",
        "value": 42,
        "nested": {"key": "value"},
        "list": [1, 2, 3],
    }


@pytest.fixture
def sample_yaml_data() -> dict[str, object]:
    """Sample YAML data for testing.
    
    Returns:
        Dictionary with sample data
    """
    return {
        "name": "test",
        "value": 42,
        "nested": {"key": "value"},
        "list": [1, 2, 3],
    }
```

### 4.4 Написання реальних тестів

Створити файл [`tests/test_easy_file.py`](../tests/test_easy_file.py):

```python
"""Tests for easy_file package."""

import pathlib

import pytest

from easy_file import File


class TestFileOpen:
    """Test File.open() method."""

    def test_open_text_default_encoding(self, temp_dir: pathlib.Path) -> None:
        """Test that text files open with UTF-8 encoding by default."""
        test_file = File(temp_dir / "test.txt")
        test_file.write_text("Привіт світ!", encoding="utf-8")
        
        with test_file.open() as f:
            content = f.read()
        
        assert content == "Привіт світ!"

    def test_open_binary_mode(self, temp_dir: pathlib.Path) -> None:
        """Test binary mode opening."""
        test_file = File(temp_dir / "test.bin")
        test_file.write_bytes(b"\x00\x01\x02")
        
        with test_file.open("rb") as f:
            content = f.read()
        
        assert content == b"\x00\x01\x02"


class TestFileCopy:
    """Test File.copy() method."""

    def test_copy_file(self, temp_dir: pathlib.Path) -> None:
        """Test copying a file."""
        source = File(temp_dir / "source.txt")
        target = File(temp_dir / "target.txt")
        
        source.write_text("test content")
        source.copy(target)
        
        assert target.exists()
        assert target.read_text() == "test content"

    def test_copy_binary_file(self, temp_dir: pathlib.Path) -> None:
        """Test copying a binary file."""
        source = File(temp_dir / "source.bin")
        target = File(temp_dir / "target.bin")
        
        source.write_bytes(b"\x00\x01\x02\x03")
        source.copy(target)
        
        assert target.exists()
        assert target.read_bytes() == b"\x00\x01\x02\x03"


class TestFileJson:
    """Test File JSON operations."""

    def test_load_json(self, temp_dir: pathlib.Path, sample_json_data: dict[str, object]) -> None:
        """Test loading JSON from file."""
        test_file = File(temp_dir / "test.json")
        test_file.write_bytes(orjson.dumps(sample_json_data))
        
        loaded = test_file.load_json()
        
        assert loaded == sample_json_data

    def test_dump_json(self, temp_dir: pathlib.Path, sample_json_data: dict[str, object]) -> None:
        """Test dumping JSON to file."""
        test_file = File(temp_dir / "test.json")
        test_file.dump_json(sample_json_data)
        
        loaded = test_file.load_json()
        
        assert loaded == sample_json_data

    def test_json_roundtrip(self, temp_dir: pathlib.Path, sample_json_data: dict[str, object]) -> None:
        """Test JSON dump and load roundtrip."""
        test_file = File(temp_dir / "test.json")
        test_file.dump_json(sample_json_data)
        loaded = test_file.load_json()
        
        assert loaded == sample_json_data


class TestFileYaml:
    """Test File YAML operations."""

    def test_load_yaml(self, temp_dir: pathlib.Path, sample_yaml_data: dict[str, object]) -> None:
        """Test loading YAML from file."""
        test_file = File(temp_dir / "test.yaml")
        test_file.write_text("name: test\nvalue: 42\nnested:\n  key: value\nlist:\n  - 1\n  - 2\n  - 3\n")
        
        loaded = test_file.load_yaml()
        
        assert loaded.data == sample_yaml_data

    def test_dump_yaml(self, temp_dir: pathlib.Path, sample_yaml_data: dict[str, object]) -> None:
        """Test dumping YAML to file."""
        test_file = File(temp_dir / "test.yaml")
        test_file.dump_yaml(sample_yaml_data)
        
        loaded = test_file.load_yaml()
        
        assert loaded.data == sample_yaml_data

    def test_yaml_roundtrip(self, temp_dir: pathlib.Path, sample_yaml_data: dict[str, object]) -> None:
        """Test YAML dump and load roundtrip."""
        test_file = File(temp_dir / "test.yaml")
        test_file.dump_yaml(sample_yaml_data)
        loaded = test_file.load_yaml()
        
        assert loaded.data == sample_yaml_data

    def test_load_yaml_with_schema(self, temp_dir: pathlib.Path) -> None:
        """Test loading YAML with schema validation."""
        from strictyaml import Map, Str, Int
        
        test_file = File(temp_dir / "test.yaml")
        test_file.write_text("name: test\nvalue: 42\n")
        
        schema = Map({"name": Str(), "value": Int()})
        loaded = test_file.load_yaml(schema)
        
        assert loaded["name"] == "test"
        assert loaded["value"] == 42

    def test_dump_yaml_with_schema(self, temp_dir: pathlib.Path) -> None:
        """Test dumping YAML with schema validation."""
        from strictyaml import Map, Str, Int
        
        test_file = File(temp_dir / "test.yaml")
        schema = Map({"name": Str(), "value": Int()})
        data: dict[str, object] = {"name": "test", "value": 42}
        
        test_file.dump_yaml(data, schema)
        
        content = test_file.read_text()
        assert "name: test" in content
        assert "value: 42" in content


class TestFileInheritance:
    """Test that File properly inherits from pathlib.Path."""

    def test_file_is_path_instance(self, temp_dir: pathlib.Path) -> None:
        """Test that File is an instance of pathlib.Path."""
        test_file = File(temp_dir / "test.txt")
        assert isinstance(test_file, pathlib.Path)

    def test_path_methods_work(self, temp_dir: pathlib.Path) -> None:
        """Test that standard pathlib methods work."""
        test_file = File(temp_dir / "subdir" / "test.txt")
        
        assert test_file.name == "test.txt"
        assert test_file.stem == "test"
        assert test_file.suffix == ".txt"
        assert "subdir" in str(test_file)
```

---

## Етап 5: CI/CD

### 5.1 Створення нового CI workflow

Створити файл [`.github/workflows/ci.yml`](../.github/workflows/ci.yml):

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    name: Test on Python ${{ matrix.python-version }}
    runs-on: ${{ matrix.os }}
    
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.12", "3.13"]
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"
      
      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          uv venv
          uv pip install -e ".[dev]"
      
      - name: Run ruff check
        run: uv run ruff check .
      
      - name: Run ruff format check
        run: uv run ruff format --check .
      
      - name: Run mypy
        run: uv run mypy src/easy_file
      
      - name: Run pytest
        run: uv run pytest --cov=easy_file --cov-report=xml --cov-report=term-missing
      
      - name: Upload coverage to Codecov
        if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.12'
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### 5.2 Оновлення release workflow

Створити файл [`.github/workflows/release.yml`](../.github/workflows/release.yml):

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  build:
    name: Build and publish
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"
      
      - name: Set up Python
        run: uv python install 3.12
      
      - name: Build package
        run: |
          uv venv
          uv pip install build
          uv run python -m build
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: dist/*
          generate_release_notes: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

---

## Етап 6: Фіналізація

### 6.1 Встановлення залежностей та налаштування середовища

```bash
# Створити віртуальне середовище з uv
uv venv

# Активувати середовище
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Встановити залежності
uv pip install -e ".[dev]"
```

### 6.2 Перевірка форматування коду

```bash
# відформатувати
uv run ruff format .
```

### 6.3 Перевірка лінтингу

```bash
# Запустити ruff check
uv run ruff check .

# Автоматично виправити можливі проблеми
uv run ruff check --fix .
```

### 6.4 Перевірка типізації

```bash
# Запустити mypy
uv run mypy src/easy_file
```

### 6.5 Запуск тестів

```bash
# Запустити всі тести
uv run pytest

# Запустити тести з покриттям
uv run pytest --cov=easy_file --cov-report=html

# Відкрити звіт про покриття
# Windows:
start htmlcov/index.html
# Linux/Mac:
open htmlcov/index.html
```

### 6.6 Налаштування pre-commit hooks

Створити файл `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

```bash
# Встановити pre-commit hooks
pre-commit install

# Перевірити hooks на всіх файлах
pre-commit run --all-files
```

### 6.7 Ініціалізація git-flow

```bash
# Переконатися, що ми на main
git checkout main

# Створити develop гілку
git checkout -b develop

# Пушнути develop
git push -u origin develop
```

### 6.8 Створення першої feature гілки

```bash
# Створити feature гілку для тестування
git-flow feature start test-new-tools

# Внести зміни, закомітити
git add .
git commit -m "feat: implement new tooling stack with uv, ruff, mypy"

# Завершити feature
git-flow feature finish test-new-tools
```

### 6.9 Перевірка CI/CD

```bash
# Пушнути зміни на develop
git push origin develop

# Створити PR з develop в main
# Перевірити, що CI проходить успішно
```

---

## Додаткові рекомендації

### A.1 Документація коду

Додати docstrings до всіх публічних методів та класів. Використовувати формат Google або NumPy.

### A.2 CHANGELOG

Створити файл `CHANGELOG.md` для відстеження змін:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Migration to uv for dependency management
- Integration of ruff for linting and formatting
- Integration of mypy for static type checking
- Implementation of git-flow branching strategy
- Comprehensive test suite with pytest
- Pre-commit hooks with ruff for automated code quality checks
- StrictYAML for safer YAML parsing with schema validation

### Changed
- Updated minimum Python version to 3.12
- Refactored File class with proper type hints
- Replaced PyYAML with StrictYAML for safer YAML operations
- Replaced old pre-commit configuration with ruff-based hooks

### Removed
- Removed poetry dependency management
- Removed mkdocs documentation
- Removed old pre-commit hooks configuration
- Removed tox configuration
- Removed flake8, isort, black configurations
- Removed PyYAML dependency
```

### A.3 CONTRIBUTING.md

Оновити файл `CONTRIBUTING.md` з новими інструкціями:

```markdown
# Contributing to easy_file

## Development Setup

1. Create virtual environment: `uv venv`
3. Install dependencies: `uv pip install -e ".[dev]"`
4. Install pre-commit hooks: `pre-commit install`
5. Run tests: `uv run pytest`
6. Format code: `uv run ruff format .`
7. Lint code: `uv run ruff check .`
8. Type check: `uv run mypy src/easy_file`

## Pre-commit Hooks

Pre-commit hooks automatically run before each commit to ensure code quality:
- Ruff linting with auto-fix
- Ruff formatting

To run hooks manually on all files:
```bash
pre-commit run --all-files
```

## Git Flow Workflow

We use git-flow for branch management:
- `main` - production releases
- `develop` - development branch
- `feature/*` - new features
- `release/*` - release preparation
- `hotfix/*` - urgent fixes
```

---

## Перевірка завершення

Перед завершенням переконайтеся, що:

- [ ] Всі старі інструменти видалені
- [ ] uv успішно встановлено та налаштовано
- [ ] ruff успішно перевіряє та формує код
- [ ] mypy успішно перевіряє типізацію
- [ ] pre-commit hooks встановлено та працюють
- [ ] Всі тести проходять
- [ ] CI/CD workflows налаштовані та працюють
- [ ] git-flow ініціалізовано
- [ ] Код відформатовано згідно з ruff
- [ ] Документація оновлена