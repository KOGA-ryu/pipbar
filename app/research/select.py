from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ResearchSelection:
    X_train: list[list[float | None]] | None
    y_train: list[float | None] | None
    X_validation: list[list[float | None]] | None
    y_validation: list[float | None] | None
    X_test: list[list[float | None]]
    y_test: list[float | None]


def select_research_inputs(
    dataset_path: str,
    feature_columns: list[str],
    target_column: str,
) -> ResearchSelection:
    dataset_dir = Path(dataset_path)
    test_path = dataset_dir / "test.csv"
    if not test_path.exists():
        raise FileNotFoundError(f"missing required dataset file: {test_path}")

    train_path = dataset_dir / "train.csv"
    validation_path = dataset_dir / "validation.csv"

    return ResearchSelection(
        X_train=_load_feature_rows(train_path, feature_columns) if train_path.exists() else None,
        y_train=_load_target_rows(train_path, target_column) if train_path.exists() else None,
        X_validation=_load_feature_rows(validation_path, feature_columns) if validation_path.exists() else None,
        y_validation=_load_target_rows(validation_path, target_column) if validation_path.exists() else None,
        X_test=_load_feature_rows(test_path, feature_columns),
        y_test=_load_target_rows(test_path, target_column),
    )


def _load_feature_rows(path: Path, feature_columns: list[str]) -> list[list[float | None]]:
    rows = _read_csv_rows(path, feature_columns)
    return [[_parse_optional_numeric(row, column) for column in feature_columns] for row in rows]


def _load_target_rows(path: Path, target_column: str) -> list[float | None]:
    rows = _read_csv_rows(path, [target_column])
    return [_parse_optional_numeric(row, target_column) for row in rows]


def _read_csv_rows(path: Path, required_columns: list[str]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    if reader.fieldnames is None:
        raise ValueError(f"missing header row in dataset file: {path}")
    missing_columns = [column for column in required_columns if column not in reader.fieldnames]
    if missing_columns:
        raise ValueError(f"missing required columns: {', '.join(missing_columns)}")

    return rows


def _parse_numeric(row: dict[str, str], column: str) -> float:
    value = row[column]
    if value == "":
        raise ValueError(f"blank numeric value in column: {column}")

    return float(value)


def _parse_optional_numeric(row: dict[str, str], column: str) -> float | None:
    value = row[column]
    if value == "":
        return None
    return float(value)
