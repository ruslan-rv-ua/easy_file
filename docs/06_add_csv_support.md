# Add CSV Support

## Context
CSV (Comma Separated Values) is a ubiquitous format for tabular data. Adding first-class support for CSV makes `easy_file` a more complete solution for general file manipulation.

## Recommendation
Implement `load_csv` and `dump_csv` methods using the Python standard `csv` library.

## Proposed Implementation

```python
import csv

    def load_csv(self, has_header: bool = True, dialect: str | csv.Dialect = "excel", **fmtparams: Any) -> list[dict[str, str]] | list[list[str]]:
        """Load CSV data from this file.

        Args:
            has_header: If True, returns list of dicts using first row as keys.
                        If False, returns list of lists.
            dialect: CSV dialect to use.
            **fmtparams: Additional formatting parameters for csv.reader/DictReader 
                         (e.g., delimiter=';').

        Returns:
            List of rows (dicts or lists of strings).
        """
        # CSV requires newline='' to handle line endings correctly
        with self.open("r", newline="", encoding="utf-8-sig") as f:
            if has_header:
                reader = csv.DictReader(f, dialect=dialect, **fmtparams)
                return list(reader)
            else:
                reader = csv.reader(f, dialect=dialect, **fmtparams)
                return list(reader)

    def dump_csv(self, data: list[dict[str, Any]] | list[list[Any]], fieldnames: list[str] | None = None, dialect: str | csv.Dialect = "excel", **fmtparams: Any) -> None:
        """Dump data to this file as CSV.
        
        Args:
            data: List of dicts or list of lists/tuples.
            fieldnames: Required if data is list of dicts and no header in data (or to enforce order).
            dialect: CSV dialect.
            **fmtparams: Formatting parameters.
        """
        self.parent.mkdir(parents=True, exist_ok=True)
        
        # Simple heuristic or use SafeToAutoRun logic
        is_dict = data and isinstance(data[0], dict)
        
        with self.atomic_write("w", encoding="utf-8", newline="") as f:
            if is_dict:
                if fieldnames is None:
                    # Infer fieldnames from the first record keys
                    if not data:
                        fieldnames = []
                    else:
                        fieldnames = list(data[0].keys())
                        
                writer = csv.DictWriter(f, fieldnames=fieldnames, dialect=dialect, **fmtparams)
                writer.writeheader()
                writer.writerows(data) # type: ignore
            else:
                writer = csv.writer(f, dialect=dialect, **fmtparams)
                writer.writerows(data) # type: ignore
```

## Note on Encoding
`encoding="utf-8-sig"` is recommended for reading CSVs to handle potential BOMs (Byte Order Marks) often found in Excel exports.
