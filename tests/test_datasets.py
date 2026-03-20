from __future__ import annotations

import csv
import shutil
from pathlib import Path

from app.datasets.dataset_runner import run_dataset_build
from app.features.feature_runner import run_feature_generation
from app.labels.label_runner import run_label_generation
from app.services.import_runner import run_import


def test_dataset_build_end_to_end_exports_research_ready_csvs(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    fixture_path = Path("tests/fixtures/valid_daily.csv")
    shutil.copy(fixture_path, input_dir / fixture_path.name)

    db_path = tmp_path / "stock_data.sqlite3"
    output_dir = tmp_path / "dataset_output"

    run_import(
        input_dir=str(input_dir),
        db_path=str(db_path),
        schema_path="app/db/schema.sql",
        import_batch_id="test-dataset-import-001",
    )
    run_feature_generation(
        db_path=str(db_path),
        ticker="VALID",
        timeframe="1d",
        start_ts=None,
        end_ts=None,
        feature_batch_id="feature-batch-dataset-001",
    )
    run_label_generation(
        db_path=str(db_path),
        ticker="VALID",
        timeframe="1d",
        start_ts=None,
        end_ts=None,
        label_batch_id="label-batch-dataset-001",
    )

    summary = run_dataset_build(
        db_path=str(db_path),
        output_path=str(output_dir),
        ticker="VALID",
        timeframe="1d",
        start_ts=None,
        end_ts=None,
        split_policy="time_70_15_15",
        selected_feature_columns=None,
        selected_label_columns=None,
        dataset_batch_id="dataset-batch-001",
    )

    assert summary == {
        "rows_selected": 4,
        "rows_assembled": 4,
        "rows_dropped_missing_features": 0,
        "rows_dropped_missing_labels": 0,
        "rows_train": 2,
        "rows_validation": 0,
        "rows_test": 2,
        "files_written": 3,
        "output_path": str(output_dir),
        "dataset_batch_id": "dataset-batch-001",
    }

    train_path = output_dir / "train.csv"
    validation_path = output_dir / "validation.csv"
    test_path = output_dir / "test.csv"

    assert train_path.exists()
    assert validation_path.exists()
    assert test_path.exists()

    with train_path.open(newline="", encoding="utf-8") as handle:
        train_rows = list(csv.DictReader(handle))
    with validation_path.open(newline="", encoding="utf-8") as handle:
        validation_rows = list(csv.DictReader(handle))
    with test_path.open(newline="", encoding="utf-8") as handle:
        test_rows = list(csv.DictReader(handle))

    assert len(train_rows) == 2
    assert len(validation_rows) == 0
    assert len(test_rows) == 2

    assert train_rows[0] == {
        "ticker": "VALID",
        "timeframe": "1d",
        "ts": "2024-01-02T00:00:00Z",
        "open": "187.15",
        "high": "188.44",
        "low": "183.89",
        "close": "185.64",
        "volume": "82488700",
        "close_1d_return": "",
        "high_low_range": "4.55",
        "close_open_delta": "-1.51",
        "next_1d_return": "-0.007488",
    }
    assert train_rows[1]["ts"] == "2024-01-03T00:00:00Z"
    assert test_rows[0]["ts"] == "2024-01-04T00:00:00Z"
    assert test_rows[1]["ts"] == "2024-01-05T00:00:00Z"
    assert test_rows[1]["next_1d_return"] == ""
