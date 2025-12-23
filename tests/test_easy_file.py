"""Tests for easy_file package."""

import pathlib

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

    def test_load_json(
        self, temp_dir: pathlib.Path, sample_json_data: dict[str, object]
    ) -> None:
        """Test loading JSON from file."""
        import orjson

        test_file = File(temp_dir / "test.json")
        test_file.write_bytes(orjson.dumps(sample_json_data))

        loaded = test_file.load_json()

        assert loaded == sample_json_data

    def test_dump_json(
        self, temp_dir: pathlib.Path, sample_json_data: dict[str, object]
    ) -> None:
        """Test dumping JSON to file."""
        test_file = File(temp_dir / "test.json")
        test_file.dump_json(sample_json_data)

        loaded = test_file.load_json()

        assert loaded == sample_json_data

    def test_json_roundtrip(
        self, temp_dir: pathlib.Path, sample_json_data: dict[str, object]
    ) -> None:
        """Test JSON dump and load roundtrip."""
        test_file = File(temp_dir / "test.json")
        test_file.dump_json(sample_json_data)
        loaded = test_file.load_json()

        assert loaded == sample_json_data


class TestFileYaml:
    """Test File YAML operations."""

    def test_load_yaml(
        self, temp_dir: pathlib.Path, sample_yaml_data: dict[str, object]
    ) -> None:
        """Test loading YAML from file."""
        test_file = File(temp_dir / "test.yaml")
        test_file.write_text(
            "name: test\nvalue: 42\nnested:\n  key: value\nlist:\n  - 1\n  - 2\n  - 3\n"
        )

        loaded = test_file.load_yaml()

        assert loaded == sample_yaml_data

    def test_dump_yaml(
        self, temp_dir: pathlib.Path, sample_yaml_data: dict[str, object]
    ) -> None:
        """Test dumping YAML to file."""
        test_file = File(temp_dir / "test.yaml")
        test_file.dump_yaml(sample_yaml_data)

        loaded = test_file.load_yaml()

        assert loaded == sample_yaml_data

    def test_yaml_roundtrip(
        self, temp_dir: pathlib.Path, sample_yaml_data: dict[str, object]
    ) -> None:
        """Test YAML dump and load roundtrip."""
        test_file = File(temp_dir / "test.yaml")
        test_file.dump_yaml(sample_yaml_data)
        loaded = test_file.load_yaml()

        assert loaded == sample_yaml_data

    def test_load_yaml_with_schema(self, temp_dir: pathlib.Path) -> None:
        """Test loading YAML with schema validation."""
        from strictyaml import Int, Map, Str

        test_file = File(temp_dir / "test.yaml")
        test_file.write_text("name: test\nvalue: 42\n")

        schema = Map({"name": Str(), "value": Int()})
        loaded = test_file.load_yaml(schema)

        assert loaded["name"] == "test"
        assert loaded["value"] == 42

    def test_dump_yaml_with_schema(self, temp_dir: pathlib.Path) -> None:
        """Test dumping YAML with schema validation."""
        from strictyaml import Int, Map, Str

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
