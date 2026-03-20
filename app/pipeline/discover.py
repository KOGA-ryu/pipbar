from __future__ import annotations

from pathlib import Path


def discover_csv_files(input_dir: str) -> list[str]:
    return sorted(
        str(path)
        for path in Path(input_dir).iterdir()
        if path.is_file() and path.suffix.lower() == ".csv"
    )
