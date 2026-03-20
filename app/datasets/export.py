from __future__ import annotations

import csv
from dataclasses import asdict
from pathlib import Path

from app.datasets.split import DatasetSplits


def export_dataset_splits(output_path: str, splits: DatasetSplits) -> dict[str, object]:
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "train.csv": splits.train,
        "validation.csv": splits.validation,
        "test.csv": splits.test,
    }

    file_paths: list[str] = []
    rows_per_file: dict[str, int] = {}
    fieldnames = [
        "ticker",
        "timeframe",
        "ts",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_1d_return",
        "high_low_range",
        "close_open_delta",
        "next_1d_return",
    ]

    for file_name, rows in files.items():
        path = output_dir / file_name
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(_format_dataset_row(asdict(row)))
        file_paths.append(str(path))
        rows_per_file[file_name] = len(rows)

    return {
        "files_written": len(files),
        "file_paths": file_paths,
        "rows_per_file": rows_per_file,
    }


def _format_dataset_row(row: dict[str, object]) -> dict[str, str]:
    return {key: _format_value(value) for key, value in row.items()}


def _format_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        formatted = f"{value:.6f}".rstrip("0").rstrip(".")
        return formatted if formatted != "-0" else "0"
    return str(value)
